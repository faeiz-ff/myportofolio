
from django.core import serializers
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, JsonResponse

from main.models import Project


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
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)
