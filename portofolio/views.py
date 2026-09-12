from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def manifesto_page(request: HttpRequest) -> HttpResponse:
    return render(request, "manifesto.html")
