
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.forms import ModelForm

from main.models import Blog, Project


def get_instances_json_view(model: type[Model]):
    return lambda request: get_instances_json(request, model)


def get_instances_json(request: HttpRequest, model: type[Model]):
    title_query = request.GET.get("title", "").strip()
    instances = model.objects.all()

    if title_query:
        instances = instances.filter(title__icontains=title_query)

    instances_json = serializers.serialize(
        'json', instances, use_natural_foreign_keys=True)
    return HttpResponse(instances_json, content_type="application/json")


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        time_range_str = project.get_time_range_str + \
            (" - dalam pembangunan" if project.is_ongoing else "")

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "git_link": project.git_link,
                "other_link": project.other_link,
                "star_count": starred_users.count(),
                "started_at": project.started_at,
                "ended_at": project.ended_at,
                "time_range_str": time_range_str,
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def get_blogs_json(request):
    title_query = request.GET.get("title", "").strip()
    blogs = Blog.objects.prefetch_related('starred_by').all()

    if title_query:
        blogs = blogs.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for blog in blogs:
        starred_users = blog.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(blog.id),
            "fields": {
                "title": blog.title,
                "text": blog.text,
                "star_count": starred_users.count(),
                "created_at": blog.created_at,
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def create_ajax(Form: type[ModelForm]):
    return lambda request: _create_ajax(request, Form)


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def _create_ajax(request: HttpRequest, Form: type[ModelForm]):
    form = Form(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
