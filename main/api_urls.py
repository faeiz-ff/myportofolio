from django.urls import path

from main.api import (
    blog_detail,
    blog_list,
    blog_star,
    experience_detail,
    experience_list,
    project_detail,
    project_list,
    project_star,
)

app_name = "api"

urlpatterns = [
    path("proyek/", project_list, name="projects"),
    path("proyek/<uuid:project_id>/", project_detail, name="project-detail"),
    path("proyek/<uuid:project_id>/star/", project_star, name="project-star"),

    path("blog/", blog_list, name="blogs"),
    path("blog/<uuid:blog_id>/", blog_detail, name="blog-detail"),
    path("blog/<uuid:blog_id>/star/", blog_star, name="blog-star"),

    path("pengalaman/", experience_list, name="experiences"),
    path("pengalaman/<uuid:experience_id>/", experience_detail, name="experience-detail"),
]
