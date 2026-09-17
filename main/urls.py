from django.urls import path

from main.views import (
    create_blog,
    delete_project,
    get_projects_json,
    show_blog_post,
    show_main,
    show_experience,
    show_project,
    show_blog,
    create_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("pengalaman/", show_experience, name="show_experience"),
    path("proyek/tambah/", create_project, name="create_project"),
    path("proyek/", show_project, name="show_project"),
    path("blog/tambah/", create_blog, name="create_blog"),
    path("blog/", show_blog, name="show_blog"),
    path("blog/<str:title>", show_blog_post, name="show_blog_post"),
    path("projects/<uuid:project_id>/delete/",
         delete_project, name="delete_project"),
    path("api/proyek/", get_projects_json, name="get_projects_json"),
]
