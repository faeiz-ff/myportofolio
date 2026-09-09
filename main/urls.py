from django.urls import path

from main.views import show_main, show_experience

app_name = "main"

urlpatterns = [
    path("tentang/", show_main, name="show_main"),
    path("pengalaman/", show_experience, name="show_experience"),
]
