from datetime import datetime, date

from django.utils.html import strip_tags
from django.utils.dateparse import parse_date
from rest_framework import serializers

from main.models import Project, Blog, Experience

class StarMixin(serializers.Serializer):
    """star_count / is_starred / starred_by_names for models with `starred_by`."""
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return any(user.id == request.user.id for user in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(StarMixin, serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)
    time_range_str = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "other_link", "git_link",
            "started_at", "ended_at", "is_ongoing", "time_range_str",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started and ended and ended < started:
            raise serializers.ValidationError(
                {"ended_at": "End date cannot be before the start date."})
        return attrs

    def get_time_range_str(self, obj):
        start = obj.started_at.strftime("%b %Y")
        if obj.is_ongoing:
            return f"{start} - Present"
        return f"{start} - {obj.ended_at.strftime('%b %Y')}"

class ExperienceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    time_range_str = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "started_at", "ended_at", "is_ongoing", "time_range_str",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started and ended and ended < started:
            raise serializers.ValidationError(
                {"ended_at": "End date cannot be before the start date."})
        return attrs

    def get_time_range_str(self, obj):
        start = obj.started_at.strftime("%b %Y")
        if obj.is_ongoing:
            return f"{start} - Present"
        return f"{start} - {obj.ended_at.strftime('%b %Y')}"


class BlogSerializer(StarMixin, serializers.ModelSerializer):
    created_at_str = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id", "title", "text", "created_at", "created_at_str",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_text(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Text cannot be empty.")
        return value

    def get_created_at_str(self, obj):
        return obj.created_at.strftime("%d %b %Y")
