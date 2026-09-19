from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe

from main.api import create_or_update_model_object, delete_model_object
from main.forms import BlogForm, ProjectForm
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


def show_experience(request):
    context = {
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_blog(request: HttpRequest):
    context = {
        "blog_list": Blog.objects.all(),
    }
    return render(request, "blog.html", context)


def show_blog_post(request: HttpRequest, title: str):
    blog = Blog.objects.get(title=title)

    html_string = markdown(blog.text)
    print(html_string)

    context = {
        "title": title,
        "created_at": blog.created_at_str,
        # DO CONSIDER THE SAFETY OF THIS HTML
        "html": mark_safe(html_string)
    }
    return render(request, "blog_post.html", context)


def create_project(request: HttpRequest):
    return create_or_update_model_object(
        request,
        ProjectForm,
        "Proyek",
        "main:show_project",
        "main:create_project",
    )


def update_project(request: HttpRequest, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return create_or_update_model_object(
        request,
        ProjectForm,
        "Proyek",
        "main:show_project",
        "main:update_project",
        project,
    )


def delete_project(request: HttpRequest, project_id):
    return delete_model_object(
        request,
        project_id,
        Project,
        "Proyek",
        "main:show_project",
    )


def create_blog(request: HttpRequest):
    return create_or_update_model_object(
        request,
        BlogForm,
        "Blog",
        "main:show_blog",
        "main:create_blog"
    )


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize('json', projects)
    return HttpResponse(projects_json, content_type="application/json")


def show_project(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)
