
from django.core import serializers
from django.db.models import Model
from django.http import HttpRequest, HttpResponse


def get_instances_json_view(model: type[Model]):
    return lambda request: get_instances_json(request, model)


def get_instances_json(request: HttpRequest, model: type[Model]):
    title_query = request.GET.get("title", "").strip()
    instances = model.objects.all()

    if title_query:
        instances = instances.filter(title__icontains=title_query)

    instances_json = serializers.serialize('json', instances)
    return HttpResponse(instances_json, content_type="application/json")
