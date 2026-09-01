from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def landing_page(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

