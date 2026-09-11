from django.urls import path

from main.views import show_main, show_experience, show_project

app_name = "main"

urlpatterns = [
    path("tentang/", show_main, name="show_main"),
    path("pengalaman/", show_experience, name="show_experience"),
    path("proyek/", show_project, name="show_project"),
]
