from django.contrib import admin
from main.models import Experience, Project, Blog

EDITOR_GROUP = "Editor"

admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(Blog)
