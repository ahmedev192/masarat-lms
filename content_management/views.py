import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import (
    Subject, Lesson, Topic, BaseContent, 
    VideoContent, DynamicContent, RevisionContent
)
from .serializers import (
    SubjectSerializer, LessonSerializer, TopicSerializer, 
    BaseContentSerializer, VideoContentSerializer, 
    DynamicContentSerializer, RevisionContentSerializer
)

# Base mixin for student authorization
class StudentAuthorizationMixin:
    permission_classes = [IsAuthenticated]

    def get_student_academic_year(self, request):
        # Get the student's academic year from the profile
        return request.user.student_profile.academic_year

# Subject List by Academic Year
class SubjectListView(StudentAuthorizationMixin, generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        academic_year = self.get_student_academic_year(self.request)
        return Subject.objects.filter(academic_year=academic_year, is_active=True)

# Subject Creation
class SubjectCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = SubjectSerializer

    def perform_create(self, serializer):
        serializer.save()

# Lessons List by Subject
class LessonListView(StudentAuthorizationMixin, generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Lesson.objects.filter(subject_id=subject_id, is_active=True).order_by('order')

# Lesson Creation
class LessonCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save()

# Topics List by Subject
# class TopicListView(StudentAuthorizationMixin, generics.ListAPIView):
#     serializer_class = TopicSerializer

#     def get_queryset(self):
#         subject_id = self.kwargs['subject_id']
#         return Topic.objects.filter(subject_id=subject_id)

# Topic Creation
class TopicCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = TopicSerializer

    def perform_create(self, serializer):
        serializer.save()

# Lesson Content by Lesson
class LessonContentView(StudentAuthorizationMixin, generics.ListAPIView):
    serializer_class = BaseContentSerializer

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return BaseContent.objects.filter(lesson_id=lesson_id)

# BaseContent Creation
class BaseContentCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = BaseContentSerializer

    def perform_create(self, serializer):
        serializer.save()



# Video Content by Lesson
class VideoContentView(StudentAuthorizationMixin, generics.ListAPIView):
    serializer_class = VideoContentSerializer

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        base_contents = BaseContent.objects.filter(lesson_id=lesson_id, content_type='VIDEO')
        return VideoContent.objects.filter(base_content__in=base_contents)

# VideoContent Creation (with File URL Handling)
class VideoContentCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = VideoContentSerializer

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        if file:
            # Store the file on the server
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'videos'))
            filename = fs.save(file.name, file)
            file_url = fs.url(os.path.join('videos', filename))
            # Save the URL in the database
            serializer.save(url=file_url)
        else:
            serializer.save()





# Dynamic Content by Lesson
class DynamicContentView(StudentAuthorizationMixin, generics.ListAPIView):
    serializer_class = DynamicContentSerializer

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        base_contents = BaseContent.objects.filter(lesson_id=lesson_id, content_type='DYNAMIC')
        return DynamicContent.objects.filter(base_content__in=base_contents)

# DynamicContent Creation
class DynamicContentCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = DynamicContentSerializer

    def perform_create(self, serializer):
        serializer.save()

# Revision Content by Topic
class RevisionContentView(StudentAuthorizationMixin, generics.ListAPIView):
    serializer_class = RevisionContentSerializer

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return RevisionContent.objects.filter(topic_id=topic_id)



# RevisionContent Creation (with File URL Handling)
class RevisionContentCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = RevisionContentSerializer

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        if file:
            # Store the file on the server
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'revisions'))
            filename = fs.save(file.name, file)
            file_url = fs.url(os.path.join('revisions', filename))
            # Save the URL in the database
            serializer.save(video_url=file_url)
        else:
            serializer.save()
