
from os import getenv
from uuid import uuid4

from django.contrib import messages
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import ModelForm


def password_correct(password: str | None) -> bool:
    if password is None:
        return False

    return password == getenv('FORM_PASSWORD')


def create_or_update_model_object(
    request: HttpRequest,
    form_model: type[ModelForm],  # I love higher order types
    model_name: str,
    exit_redirect: str,
    view_name: str,
    form_instance: Model | None = None,
):
    form = form_model(request.POST or None, instance=form_instance)

    if request.method == 'POST' and form.is_valid():
        # form_model needs to have the shape of main.forms.ProtectedForm, Hacky
        # Refer to main.forms.ProtectedForm. TODO: swap with proper auth
        if not password_correct(form.data['password']):
            messages.error(request, "Password salah, data tidak ditambahkan")
            return redirect(view_name)

        print(form.cleaned_data)
        form.save()
        messages.success(request,
                         "data " + model_name + " baru berhasil ditambahkan!")
        return redirect(exit_redirect)

    context = {
        'name': 'Faeiz Faiza Fasha',
        'form': form,
        'model_name': model_name,
        'exit_redirect': exit_redirect,
        'view_name': view_name,
        'form_instance': str(form_instance.id
                             if form_instance is not None else ""),
    }

    return render(request, "model_form.html", context)


def delete_model_object(
        request: HttpRequest,
        object_id: uuid4,
        model: type[Model],
        model_name: str,
        view_name: str,
):
    # TODO: swap with proper auth
    password = request.POST.get("password")

    model_object = get_object_or_404(model, pk=object_id)

    if request.method == "POST":
        if not password_correct(password):
            messages.error(request,
                           "Password salah, " + model_name + " tidak dihapus")
            return redirect(view_name)

        model_object.delete()
        messages.success(request, model_name + " berhasil dihapus!")
        return redirect(view_name)

    return redirect(view_name)
