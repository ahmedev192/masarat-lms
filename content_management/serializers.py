from rest_framework import serializers
from .models import Subject, Lesson, Topic, BaseContent, VideoContent, DynamicContent, RevisionContent

# Subject Serializer
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'academic_year', 'description', 'is_active']


# Lesson Serializer
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'subject', 'order', 'description', 'is_active','duration']


# Topic Serializer
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'subject', 'description', 'topic_difficulty_level']


# BaseContent Serializer
class BaseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseContent
        fields = ['id', 'lesson', 'description', 'content_type', 'learning_type']


# VideoContent Serializer
class VideoContentSerializer(serializers.ModelSerializer):
    base_content_id = serializers.PrimaryKeyRelatedField(
        queryset=BaseContent.objects.all(), source='base_content', write_only=True
    )
    base_content = BaseContentSerializer(read_only=True)

    class Meta:
        model = VideoContent
        fields = ['id', 'base_content', 'base_content_id']

    def create(self, validated_data):
        return VideoContent.objects.create(**validated_data)


# DynamicContent Serializer
class DynamicContentSerializer(serializers.ModelSerializer):
    base_content = BaseContentSerializer()

    class Meta:
        model = DynamicContent
        fields = ['id', 'base_content', 'content_url']



# RevisionContent Serializer
class RevisionContentSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), source='topic', write_only=True
    )
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = RevisionContent
        fields = ['id', 'topic', 'topic_id']

    def create(self, validated_data):
        return RevisionContent.objects.create(**validated_data)