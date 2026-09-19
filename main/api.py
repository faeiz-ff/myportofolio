
from os import getenv
from uuid import uuid4

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import ModelForm


def password_correct(password: str | None) -> bool:
    if password is None:
        return False

    return password == getenv('FORM_PASSWORD')


def create_model_object(
    request: HttpRequest,
    form_model: type[ModelForm],  # I love higher order types
    form_name: str,
    form_redirect: str,
    form_create: str,
):
    form = form_model(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # form_model needs to have the shape of main.forms.ProtectedForm, Hacky
        # Refer to main.forms.ProtectedForm. TODO: swap with proper auth
        if not password_correct(form.data['password']):
            messages.error(request, "Password salah, data tidak ditambahkan")
            return redirect(form_create)

        form.save()
        messages.success(request, form_name + " baru berhasil ditambahkan!")
        return redirect(form_redirect)

    context = {
        'name': 'Faeiz Faiza Fasha',
        'form': form,
        'form_name': form_name,
        'form_redirect': form_redirect,
        'form_create': form_create,
    }

    return render(request, "model_form.html", context)


def delete_model_object(
        request: HttpRequest,
        object_id: uuid4,
        model: type[ModelForm],
        model_name: str,
        redirect_name: str,
):
    # TODO: swap with proper auth
    password = request.POST.get("password")

    model_object = get_object_or_404(model, pk=object_id)

    if request.method == "POST":
        if not password_correct(password):
            messages.error(request,
                           "Password salah, " + model_name + " tidak dihapus")
            return redirect(redirect_name)

        model_object.delete()
        messages.success(request, model_name + " berhasil dihapus!")
        return redirect(redirect_name)

    return redirect(redirect_name)
