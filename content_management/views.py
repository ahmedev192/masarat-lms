import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import (
    Subject, Lesson, Topic, BaseContent, 
    VideoContent, DynamicContent, RevisionContent,ContentType
)
from .serializers import (
    SubjectSerializer, LessonSerializer, TopicSerializer, 
    ContentSerializer, VideoContentSerializer, 
    DynamicContentSerializer, RevisionContentSerializer
)
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

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
    serializer_class = ContentSerializer

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        
        # Get base contents and prefetch related video or dynamic content based on type
        base_contents = BaseContent.objects.filter(lesson_id=lesson_id).prefetch_related(
            Prefetch(
                'video_content',  # Use the related_name defined in VideoContent
                queryset=VideoContent.objects.all(),
                to_attr='video_contents'  # This will be a single object due to OneToOneField
            ),
            Prefetch(
                'dynamic_content',  # Use the related_name defined in DynamicContent
                queryset=DynamicContent.objects.all(),
                to_attr='dynamic_contents'  # This will be a single object due to OneToOneField
            )
        )
        return base_contents

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_data = []

        for base_content in queryset:
            content_data = ContentSerializer(base_content).data
            # Append related content based on content type
            if base_content.content_type == ContentType.VIDEO:
                content_data['video_contents'] = VideoContentSerializer(
                    base_content.video_content  # Accessing single object now
                ).data if base_content.video_content else None
            elif base_content.content_type == ContentType.DYNAMIC:
                content_data['dynamic_contents'] = DynamicContentSerializer(
                    base_content.dynamic_content  # Accessing single object now
                ).data if base_content.dynamic_content else None
            response_data.append(content_data)

        return Response(response_data, status=status.HTTP_200_OK)

# BaseContent Creation with Video/Dynamic Content Handling
class ContentCreateView(StudentAuthorizationMixin, generics.CreateAPIView):
    serializer_class = ContentSerializer

    def perform_create(self, serializer):
        # Save the base content
        base_content = serializer.save()

        # Check content_type and handle content specifics
        content_type = self.request.data.get("content_type")

        if content_type == ContentType.VIDEO:
            file = self.request.FILES.get("file")
            if file:
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "videos"))
                filename = fs.save(file.name, file)
                file_url = fs.url(os.path.join("videos", filename))

                # Create associated VideoContent
                VideoContent.objects.create(base_content=base_content, url=file_url)
            else:
                raise serializers.ValidationError({"file": "Video file is required for VIDEO content type"})

        elif content_type == ContentType.DYNAMIC:
            file = self.request.FILES.get("file")
            if file:
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "web_pages"))
                filename = fs.save(file.name, file)
                file_url = fs.url(os.path.join("web_pages", filename))

                # Create associated DynamicContent
                DynamicContent.objects.create(base_content=base_content, url=file_url)
            else:
                raise serializers.ValidationError({"file": "File is required for DYNAMIC content type"})

        else:
            raise serializers.ValidationError({"content_type": "Invalid content type provided."})



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
