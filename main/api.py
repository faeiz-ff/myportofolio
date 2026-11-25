from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Blog, Experience, Project
from main.permissions import IsPortfolioOwnerOrReadOnly
from main.serializers import (
    BlogSerializer, ExperienceSerializer, ProjectSerializer,
)

AUTH = [SessionAuthentication, TokenAuthentication]

READ = ("GET", "HEAD")


# ---------- Shared helpers ----------

def _list_or_create(request, queryset, serializer_class):
    """GET/HEAD: list (optional ?title=). POST: create."""
    context = {"request": request}

    if request.method in READ:
        title = request.query_params.get("title", "").strip()
        if title:
            queryset = queryset.filter(title__icontains=title)
        return Response(serializer_class(queryset, many=True, context=context).data)

    serializer = serializer_class(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _retrieve_update_delete(request, instance, serializer_class):
    """GET/HEAD: retrieve. PUT/PATCH: update. DELETE: remove."""
    context = {"request": request}

    if request.method in READ:
        return Response(serializer_class(instance, context=context).data)

    if request.method == "DELETE":
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = serializer_class(
        instance, data=request.data, partial=request.method == "PATCH",
        context=context,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def _toggle_star(request, instance, serializer_class):
    if instance.starred_by.filter(pk=request.user.pk).exists():
        instance.starred_by.remove(request.user)
    else:
        instance.starred_by.add(request.user)
    return Response(serializer_class(instance, context={"request": request}).data)


# ---------- Auth ----------

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    if request.auth is not None:
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Project ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes(AUTH)
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    queryset = Project.objects.prefetch_related("starred_by").order_by("title", "id")
    return _list_or_create(request, queryset, ProjectSerializer)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes(AUTH)
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id)
    return _retrieve_update_delete(request, project, ProjectSerializer)


@api_view(["POST"])
@authentication_classes(AUTH)
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id)
    return _toggle_star(request, project, ProjectSerializer)


# ---------- Experience ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes(AUTH)
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_list(request):
    """Extra filter: ?category=internship|research|volunteer|part-time|full-time|freelance."""
    queryset = Experience.objects.order_by("-started_at", "id")
    category = request.query_params.get("category", "").strip()
    if category and request.method in READ:
        queryset = queryset.filter(category=category)
    return _list_or_create(request, queryset, ExperienceSerializer)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes(AUTH)
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    return _retrieve_update_delete(request, experience, ExperienceSerializer)


# ---------- Blog ----------

@api_view(["GET", "HEAD", "POST"])
@authentication_classes(AUTH)
@permission_classes([IsPortfolioOwnerOrReadOnly])
def blog_list(request):
    queryset = Blog.objects.prefetch_related("starred_by").order_by("-created_at", "id")
    return _list_or_create(request, queryset, BlogSerializer)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes(AUTH)
@permission_classes([IsPortfolioOwnerOrReadOnly])
def blog_detail(request, blog_id):
    blog = get_object_or_404(
        Blog.objects.prefetch_related("starred_by"), pk=blog_id)
    return _retrieve_update_delete(request, blog, BlogSerializer)


@api_view(["POST"])
@authentication_classes(AUTH)
@permission_classes([IsAuthenticated])
def blog_star(request, blog_id):
    blog = get_object_or_404(
        Blog.objects.prefetch_related("starred_by"), pk=blog_id)
    return _toggle_star(request, blog, BlogSerializer)
