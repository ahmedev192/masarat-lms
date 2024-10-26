from django.urls import path
from .views import (
    SubjectListView, SubjectCreateView,
    LessonListView, LessonCreateView, TopicCreateView,
    LessonContentView, BaseContentCreateView,
    VideoContentView, VideoContentCreateView,
    DynamicContentView, DynamicContentCreateView,
    RevisionContentView, RevisionContentCreateView
)

urlpatterns = [
    # Subjects
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject-create'),

    # Lessons
    path('subjects/<uuid:subject_id>/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),

    # Topics
    # path('subjects/<uuid:subject_id>/topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/create/', TopicCreateView.as_view(), name='topic-create'),

    # Lesson Content
    path('lessons/<uuid:lesson_id>/contents/', LessonContentView.as_view(), name='lesson-content-list'),
    path('contents/create/', BaseContentCreateView.as_view(), name='base-content-create'),

    # Video Content
    path('lessons/<uuid:lesson_id>/video-content/', VideoContentView.as_view(), name='video-content-list'),
    path('video-content/create/', VideoContentCreateView.as_view(), name='video-content-create'),

    # Dynamic Content
    path('lessons/<uuid:lesson_id>/dynamic-content/', DynamicContentView.as_view(), name='dynamic-content-list'),
    path('dynamic-content/create/', DynamicContentCreateView.as_view(), name='dynamic-content-create'),

    # Revision Content
    path('topics/<uuid:topic_id>/revision-content/', RevisionContentView.as_view(), name='revision-content-list'),
    path('revision-content/create/', RevisionContentCreateView.as_view(), name='revision-content-create'),
]
