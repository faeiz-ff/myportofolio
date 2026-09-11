import uuid
from datetime import date
import django
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField(default=django.utils.timezone.now)
    ended_at = models.DateField(null=True)

    def __str__(self) -> str:
        return str(self.title)

    @property
    def is_ongoing(self) -> bool:
        if self.ended_at is None:
            return True

        return self.ended_at > date.today()

    @property
    def get_time_range_str(self) -> str:
        time_str = self.started_at.strftime("%b %Y")
        if self.ended_at is not None:
            time_str += self.ended_at.strftime(
                " - %b %Y") if not self.is_ongoing else ""

        return time_str


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    git_link = models.URLField(null=False)
    other_link = models.URLField(null=False)
    description = models.TextField()
    started_at = models.DateField(default=django.utils.timezone.now)
    ended_at = models.DateField(null=True)

    @property
    def has_other_link(self) -> bool:
        if self.other_link == "":
            return False
        return True

    @property
    def is_ongoing(self) -> bool:
        if self.ended_at is None:
            return True

        return self.ended_at > date.today()

    @property
    def get_time_range_str(self) -> str:
        time_str = self.started_at.strftime("%b %Y")
        if self.ended_at is not None:
            time_str += self.ended_at.strftime(
                " - %b %Y") if not self.is_ongoing else ""

        return time_str
