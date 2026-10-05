from django.urls import include, path

from main.api import get_instances_json_view, get_projects_json

from main.views import (
    create_project_ajax,
    create_view,
    update_view,
    delete_view,
    show_main,
    show_experience,
    show_projects,
    show_blog,
    show_blog_post,
    show_root,

    register,
    login_user,
    logout_user,
    toggle_star_view,
)

from main.models import Experience, Project, Blog

app_name = "main"

project = (
    [
        path("", show_projects, name="show"),
        path("tambah/", create_view('project'), name="create"),
        path("<uuid:instance_id>/ubah/", update_view('project'), name="update"),
        path("<uuid:instance_id>/hapus/", delete_view('project'), name="delete"),
        path("<uuid:instance_id>/star/", toggle_star_view('project'), name="toggle_star"),
        path("add-ajax/", create_project_ajax, name="ajax"),
    ],
    "project"
)

experience = (
    [
        path("", show_experience, name="show"),
        path("tambah/", create_view('experience'), name="create"),
        path("<uuid:instance_id>/ubah/",
             update_view('experience'), name="update"),
        path("<uuid:instance_id>/hapus/",
             delete_view('experience'), name="delete"),
    ],
    "experience"
)


blog = (
    [
        path("", show_blog, name="show"),
        path("tambah/", create_view('blog'), name="create"),
        path("<uuid:instance_id>/ubah/", update_view('blog'), name="update"),
        path("<uuid:instance_id>/hapus/", delete_view('blog'), name="delete"),
        path("title/<str:title>/", show_blog_post, name="show_post"),
        path("<uuid:instance_id>/star/", toggle_star_view('blog'), name="toggle_star"),
    ],
    "blog"
)


api = (
    [
        path("proyek/", get_projects_json, name="get_projects_json"),
        path("blog/", get_instances_json_view(Blog), name="get_blogs_json"),
        path("pengalaman/", get_instances_json_view(Experience),
             name="get_experiences_json"),
    ],
    "api"
)

urlpatterns = [
    path("", show_main, name="show_main"),
    path("root/", show_root, name="root"),
    path("pengalaman/", include(experience)),
    path("proyek/", include(project)),
    path("blog/", include(blog)),
    path("api/", include(api)),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]
