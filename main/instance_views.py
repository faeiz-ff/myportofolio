
from uuid import UUID
from dataclasses import dataclass

from django.contrib import messages
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import ModelForm

from main.forms import ExperienceForm, ProjectForm, BlogForm
from main.models import Experience, Project, Blog
from django.contrib.auth.decorators import login_required, user_passes_test


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

    'experience': ModelViewInfo(
        Experience,
        ExperienceForm,
        'main:experience:create',
        'main:experience:show',
        'main:experience:update',
        'main:experience:delete',
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


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.is_superuser)
def create_instance(
    request: HttpRequest,
    model_name: str,
):
    model_info = MODEL_VIEW_INFO[model_name]

    form = model_info.form(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, model_name + " baru berhasil ditambahkan.")
        return redirect(model_info.view_read)

    context = {
        'name': 'Faeiz Faiza Fasha',
        'form': form,
        'model_name': model_name,
        'exit_redirect': model_info.view_read,
        'view_name': model_info.view_create,
    }

    return render(request, "model_create_form.html", context)


@login_required(login_url="/login/")
def update_instance(
    request: HttpRequest,
    model_name: str,
    instance_id: UUID,
):
    model_info = MODEL_VIEW_INFO[model_name]

    instance = get_object_or_404(model_info.model, pk=instance_id)
    form = model_info.form(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, model_name + " berhasil diubah.")
        return redirect(model_info.view_read)

    context = {
        'name': 'Faeiz Faiza Fasha',
        'form': form,
        'model_name': model_name,
        'exit_redirect': model_info.view_read,
        'view_name': model_info.view_update,
        'form_instance': instance_id,
    }

    return render(request, "model_update_form.html", context)


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.is_superuser)
def delete_instance(
    request: HttpRequest,
    model_name: str,
    object_id: UUID,
):
    model_info = MODEL_VIEW_INFO[model_name]

    if request.method == "POST":
        instance = get_object_or_404(model_info.model, pk=object_id)
        instance.delete()
        messages.success(request, model_name + " berhasil dihapus.")
        return redirect(model_info.view_read)

    return redirect(model_info.view_read)
