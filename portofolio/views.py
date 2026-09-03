from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def landing_page(_: HttpRequest) -> HttpResponse:
    return redirect('manifesto_page')


def manifesto_page(request: HttpRequest) -> HttpResponse:
    return render(request, "manifesto.html")
