from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def landing_page(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def manifesto_page(request: HttpRequest) -> HttpResponse:
    return render(request, "manifesto.html")


def about_page(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")


def project_page(request: HttpRequest) -> HttpResponse:
    return render(request, "project.html")
