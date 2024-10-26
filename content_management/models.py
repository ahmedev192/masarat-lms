import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Define enums as choices
class AcademicYear(models.TextChoices):
    PRIMARY_1 = 'Primary 1', 'Primary Year 1'
    PRIMARY_2 = 'Primary 2', 'Primary Year 2'
    PRIMARY_3 = 'Primary 3', 'Primary Year 3'
    PRIMARY_4 = 'Primary 4', 'Primary Year 4'
    PRIMARY_5 = 'Primary 5', 'Primary Year 5'
    PRIMARY_6 = 'Primary 6', 'Primary Year 6'

    PREP_1 = 'Prep 1', 'Prep Year 1'
    PREP_2 = 'Prep 2', 'Prep Year 2'
    PREP_3 = 'Prep 3', 'Prep Year 3'

    SECONDARY_1 = 'Secondary 1', 'Secondary Year 1'
    SECONDARY_2 = 'Secondary 2', 'Secondary Year 2'
    SECONDARY_3 = 'Secondary 3', 'Secondary Year 3'

class LearningType(models.TextChoices):
    VISUAL = 'Visual', 'Visual'
    AUDITORY = 'Auditory', 'Auditory'
    KINESTHETIC = 'Kinesthetic', 'Kinesthetic'
    READING_WRITING = 'Reading/Writing', 'Reading/Writing'

class ContentType(models.TextChoices):
    VIDEO = 'VIDEO', 'Video'
    DYNAMIC = 'DYNAMIC', 'Dynamic'

class DifficultyLevel(models.TextChoices):
    BEGINNER = 'BEGINNER', 'Beginner'
    INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
    ADVANCED = 'ADVANCED', 'Advanced'


# Models
class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    academic_year = models.CharField(
        max_length=20, choices=AcademicYear.choices, null=False, blank=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()
    duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    topic_difficulty_level = models.CharField(
        max_length=12, choices=DifficultyLevel.choices, null=False, blank=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BaseContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    learning_type = models.CharField(
        max_length=15, choices=LearningType.choices, null=False, blank=False
    )
    content_type = models.CharField(
        max_length=10, choices=ContentType.choices, unique=False, null=False, blank=False
    )
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Content {self.id} for Lesson {self.lesson}"

class VideoContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_content = models.OneToOneField(
        BaseContent,
        on_delete=models.CASCADE,
        related_name='video_content'  # Define related name
    )
    url = models.TextField()

    def __str__(self):
        return f"VideoContent {self.id}"

class DynamicContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_content = models.OneToOneField(
        BaseContent,
        on_delete=models.CASCADE,
        related_name='dynamic_content'  # Define related name
    )
    url = models.TextField()

    def __str__(self):
        return f"DynamicContent {self.id}"


class RevisionContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    video_url = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RevisionContent {self.id} for Topic {self.topic}"
