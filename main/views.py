from uuid import uuid4

from django.core import serializers
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.safestring import mark_safe

from main.api import get_instances_json
from main.instance_views import create_or_update_instance, delete_instance
from main.models import Blog, Experience, Project

from markdown import markdown


def show_main(request):
    context = {
        "name": "Faeiz Faiza Fasha",
        "npm": "2506602196",
        "study_program": "S1 Ilmu Komputer",
        "bio": mark_safe(
            """
            Seniman, insinyur perangkat lunak, pemrogram rekreasional.<br>
            Cinta dengan semua teori komputasi sejak saya baru lahir.<br>
            Tertarik dengan systems programming, teknik kompilator.<br>
            Suka berbahasa <a href=\"https://ziglang.org\" >Zig</a>
            dan <a href=\"https://typescriptlang.org\">TypeScript</a>;
            mengenali banyak bahasa lain.<br> Selamanya pelajar.
            """
        ),  # DO CONSIDER THE SAFETY OF THIS HTML
    }
    return render(request, "about.html", context)


def show_instances(request: HttpRequest, model: type[Model], template: str):
    json_response = get_instances_json(request, model)

    instances = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    instances = [instance.object for instance in instances]
    title_query = request.GET.get("title", "").strip()

    context = {
        "instance_list": instances,
        "title_query": title_query,
    }

    return render(request, template, context)


def show_blog(request: HttpRequest):
    return show_instances(request, Blog, "blog.html")


def show_project(request: HttpRequest):
    context = {
        "instance_list": Project.objects.all(),
    }
    return render(request, "project.html", context)


def show_experience(request):
    context = {
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_blog_post(request: HttpRequest, title: str):
    blog = Blog.objects.get(title=title)

    html_string = markdown(blog.text)

    context = {
        "title": title,
        "created_at": blog.created_at_str,
        # DO CONSIDER THE SAFETY OF THIS HTML
        "html": mark_safe(html_string),
        "blog": blog,
    }
    return render(request, "blog_post.html", context)


def delete_view(model_name: str):
    def inner(request: HttpRequest, instance_id: uuid4):
        return delete_instance(request, model_name, instance_id)
    return inner


def create_view(model_name: str):
    def inner(request: HttpRequest):
        return create_or_update_instance(request, model_name)
    return inner


def update_view(model_name: str):
    def inner(request: HttpRequest, instance_id: uuid4):
        return create_or_update_instance(request, model_name, instance_id)
    return inner


def show_root(request: HttpRequest):
    context = {
        'projects': Project.objects.all(),
        'blogs': Blog.objects.all(),
    }

    return render(request, 'root.html', context)
