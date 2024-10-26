from django.contrib import admin
from .models import Subject, Lesson, Topic, BaseContent, VideoContent, DynamicContent, RevisionContent

# Registering models with default admin interface
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Topic)
admin.site.register(BaseContent)
admin.site.register(VideoContent)
admin.site.register(DynamicContent)
admin.site.register(RevisionContent)
