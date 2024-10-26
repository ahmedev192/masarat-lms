from django.urls import path
from .views import (
    SubjectListView, SubjectCreateView,
    LessonListView, LessonCreateView, TopicCreateView,
    LessonContentView, ContentCreateView,
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
    path('topics/create/', TopicCreateView.as_view(), name='topic-create'),

    # Lesson Content
    path('lessons/<uuid:lesson_id>/contents/', LessonContentView.as_view(), name='lesson-content-list'),
    path('contents/create/', ContentCreateView.as_view(), name='content-create'),

    # Revision Content
    path('topics/<uuid:topic_id>/revision-content/', RevisionContentView.as_view(), name='revision-content-list'),
    path('revision-content/create/', RevisionContentCreateView.as_view(), name='revision-content-create'),
]
