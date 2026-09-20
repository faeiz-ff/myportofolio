from django.urls import include, path

from main.views import (
    create_view,
    update_view,
    delete_view,

    get_projects_json,

    show_main,
    show_experience,
    show_project,
    show_blog,
    show_blog_post,
)

app_name = "main"

project = (
    [
        path("", show_project, name="show"),
        path("tambah/", create_view('project'), name="create"),
        path("<uuid:instance_id>/ubah/", update_view('project'), name="update"),
        path("<uuid:instance_id>/hapus/", delete_view('project'), name="delete"),
    ],
    "project"
)


blog = (
    [
        path("", show_blog, name="show"),
        path("tambah/", create_view('blog'), name="create"),
        path("<uuid:instance_id>/ubah/", update_view('blog'), name="update"),
        path("<uuid:instance_id>/hapus/", delete_view('blog'), name="delete"),
        path("title/<str:title>/", show_blog_post, name="show_post"),
    ],
    "blog"
)


api = (
    [
        path("proyek/", get_projects_json, name="get_projects_json"),
    ],
    "api"
)

urlpatterns = [
    path("", show_main, name="show_main"),
    path("pengalaman/", show_experience, name="show_experience"),
    path("proyek/", include(project)),
    path("blog/", include(blog)),
    path("api/", include(api))
]
