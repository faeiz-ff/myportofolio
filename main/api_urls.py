from django.urls import include, path

from main.models import Experience
from main.api import (
    get_instances_json_view,
    get_projects_json,
    get_blogs_json,
    create_ajax,
    project_detail,
    project_list,
)

app_name = "api"

urlpatterns = [
    path("proyek/", project_list, name="get_projects_json"),
    path("proyek/<uuid:project_id>/", project_detail, name="project-detail"),
    path("blog/", get_blogs_json, name="get_blogs_json"),
    path("pengalaman/", get_instances_json_view(Experience),
         name="get_experiences_json"),
]
