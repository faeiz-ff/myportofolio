from django.urls import path

from main.views import show_blog_post, show_main, show_experience, \
    show_project, \
    show_blog

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("pengalaman/", show_experience, name="show_experience"),
    path("proyek/", show_project, name="show_project"),
    path("blog/", show_blog, name="show_blog"),
    path("blog/<str:title>", show_blog_post, name="show_blog_post"),
]
