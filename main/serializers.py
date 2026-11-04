from datetime import datetime, date

from django.utils.html import strip_tags
from django.utils.dateparse import parse_date
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    time_range_str = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "other_link",
            "git_link", "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
            "time_range_str",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_started_at(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

    def _format_date(self, value):
        if not value:
            return None

        # THIS IS WHAT HAPPENS TO A TYPE UNSAFE LANGUAGE
        # LOOK
        # LOOK AT THIS
        if isinstance(value, str):
            value = parse_date(value)

        if isinstance(value, (date, datetime)):
            return value.strftime("%b %Y")
        return None

    def get_time_range_str(self, obj):
        start = self._format_date(obj.started_at)
        if not start:
            return ""

        if getattr(obj, "is_ongoing", False):
            return f"{start} - Present"

        end = self._format_date(obj.ended_at)
        if end:
            return f"{start} - {end}"

        return start
