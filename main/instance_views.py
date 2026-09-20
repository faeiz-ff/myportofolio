
from os import getenv
from uuid import uuid4
from dataclasses import dataclass

from django.contrib import messages
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import ModelForm

from main.forms import ProjectForm, BlogForm
from main.models import Project, Blog


@dataclass
class ModelViewInfo:
    model: type[Model]
    form: type[ModelForm]
    view_create: str
    view_read: str
    view_update: str
    view_delete: str


MODEL_VIEW_INFO = {
    'project': ModelViewInfo(
        Project,
        ProjectForm,
        'main:project:create',
        'main:project:show',
        'main:project:update',
        'main:project:delete',
    ),

    'blog': ModelViewInfo(
        Blog,
        BlogForm,
        'main:blog:create',
        'main:blog:show',
        'main:blog:update',
        'main:blog:delete',
    ),
}


def password_correct(password: str | None) -> bool:
    if password is None:
        return False

    return password == getenv('FORM_PASSWORD')


def create_or_update_instance(
    request: HttpRequest,
    model_name: str,
    instance_id: uuid4 | None = None,
):
    model_info = MODEL_VIEW_INFO[model_name]

    instance = get_object_or_404(model_info.model, pk=instance_id) \
        if instance_id else None

    form = model_info.form(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        # form_model needs to have the shape of main.forms.ProtectedForm, Hacky
        # Refer to main.forms.ProtectedForm. TODO: swap with proper auth
        if not password_correct(form.data['password']):
            messages.error(request, "Password salah, data tidak ditambahkan")
            if instance_id:
                return redirect(model_info.view_update, instance_id)
            else:
                return redirect(model_info.view_create)

        form.save()
        messages.success(request,
                         "data " + model_name + " baru berhasil ditambahkan!")
        return redirect(model_info.view_read)

    context = {
        'name': 'Faeiz Faiza Fasha',
        'form': form,
        'model_name': model_name,
        'exit_redirect': model_info.view_read,
        'view_name':
            model_info.view_update
            if instance_id else model_info.view_create,
        'form_instance': instance_id,
    }

    return render(request, "model_form.html", context)


def delete_instance(
        request: HttpRequest,
        model_name: str,
        object_id: uuid4,
):
    model_info = MODEL_VIEW_INFO[model_name]

    if request.method == "POST":
        # TODO: swap with proper auth
        password = request.POST.get("password")

        instance = get_object_or_404(model_info.model, pk=object_id)

        if not password_correct(password):
            messages.error(request,
                           "Password salah, " + model_name + " tidak dihapus")
            return redirect(model_info.view_read)

        instance.delete()
        messages.success(request, model_name + " berhasil dihapus!")
        return redirect(model_info.view_read)

    return redirect(model_info.view_read)
