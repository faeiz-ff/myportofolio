from uuid import UUID

from django.core import serializers
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from main.admin import EDITOR_GROUP
from main.forms import ProjectForm, BlogForm
from main.instance_views import (
    group_required,
    create_instance,
    update_instance,
    delete_instance,
    toggle_star
)

from markdown import markdown
import datetime


from main.models import Blog, Experience, Project
from main.serializers import (
    BlogSerializer, ExperienceSerializer, ProjectSerializer,
)

def _filter_by_title(request: HttpRequest, queryset):
    title = request.GET.get("title", "").strip()
    return queryset.filter(title__icontains=title) if title else queryset


def get_projects_data(request: HttpRequest) -> list[dict]:
    queryset = _filter_by_title(
        request, Project.objects.prefetch_related("starred_by").order_by("title", "id"))
    return list(ProjectSerializer(queryset, many=True, context={"request": request}).data)


def get_experiences_data(request: HttpRequest) -> list[dict]:
    queryset = _filter_by_title(
        request, Experience.objects.order_by("-started_at", "id"))
    return list(ExperienceSerializer(queryset, many=True, context={"request": request}).data)


def get_blogs_data(request: HttpRequest) -> list[dict]:
    queryset = _filter_by_title(
        request, Blog.objects.prefetch_related("starred_by").order_by("-created_at", "id"))
    return list(BlogSerializer(queryset, many=True, context={"request": request}).data)


def show_instances(request: HttpRequest, get_data, template: str):
    context = {
        "instance_list": get_data(request),
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, template, context)

def show_main(request):
    last_login = request.COOKIES.get(
        'last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
    }
    return render(request, "about.html", context)



def show_projects(request: HttpRequest):
    title_query = request.GET.get("title", "").strip()

    context = {
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


def show_blog(request: HttpRequest):
    title_query = request.GET.get("title", "").strip()

    context = {
        "title_query": title_query,
        "form": BlogForm(),
    }
    return render(request, "blog.html", context)


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
    def inner(request: HttpRequest, instance_id: UUID):
        return delete_instance(request, model_name, instance_id)
    return inner


def create_view(model_name: str):
    def inner(request: HttpRequest):
        return create_instance(request, model_name)
    return inner


def update_view(model_name: str):
    def inner(request: HttpRequest, instance_id: UUID):
        return update_instance(request, model_name, instance_id)
    return inner


def toggle_star_view(model_name: str):
    def inner(request: HttpRequest, instance_id: UUID):
        return toggle_star(request, model_name, instance_id)
    return inner


@login_required(login_url="/login/")
@group_required(EDITOR_GROUP)
def show_root(request: HttpRequest):
    context = {
        'projects': Project.objects.all(),
        'experiences': Experience.objects.all(),
        'blogs': Blog.objects.all(),
    }

    return render(request, 'root.html', context)


def register(request: HttpRequest):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Faeiz Faiza Fasha",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie(
            'last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Faeiz Faiza Fasha",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


