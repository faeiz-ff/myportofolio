from django.http import HttpRequest
from django.shortcuts import render
from django.utils.safestring import mark_safe

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


def show_project(request):
    context = {
        "project_list": Project.objects.all(),
    }

    return render(request, "project.html", context)


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
