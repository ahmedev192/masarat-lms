from rest_framework import serializers
from .models import Subject, Lesson, Topic, BaseContent, VideoContent, DynamicContent, RevisionContent

# Subject Serializer
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'code', 'description', 'is_active', 
            'academic_year', 'created_at', 'updated_at'
        ]


# Lesson Serializer
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'subject', 'description', 'order', 
            'duration', 'is_active', 'created_at', 'updated_at'
        ]


# Topic Serializer
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'id', 'name', 'subject', 'description', 
            'topic_difficulty_level', 'created_at', 'updated_at'
        ]


# VideoContent Serializer
class VideoContentSerializer(serializers.ModelSerializer):
    base_content_id = serializers.PrimaryKeyRelatedField(
        queryset=BaseContent.objects.all(), source='base_content', write_only=True
    )
    base_content = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VideoContent
        fields = ['id', 'base_content', 'base_content_id', 'url']


# DynamicContent Serializer
class DynamicContentSerializer(serializers.ModelSerializer):
    base_content_id = serializers.PrimaryKeyRelatedField(
        queryset=BaseContent.objects.all(), source='base_content', write_only=True
    )
    base_content = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DynamicContent
        fields = ['id', 'base_content', 'base_content_id', 'url']


# BaseContent Serializer
class ContentSerializer(serializers.ModelSerializer):
    # Make video_contents and dynamic_contents writable
    video_contents = VideoContentSerializer(many=False, required=False)
    dynamic_contents = DynamicContentSerializer(many=False, required=False)

    class Meta:
        model = BaseContent
        fields = [
            'id', 'lesson', 'learning_type', 'content_type', 
            'description', 'created_at', 'updated_at', 
            'video_contents', 'dynamic_contents'
        ]

    def create(self, validated_data):
        # Pop nested data for video_contents and dynamic_contents if provided
        video_content_data = validated_data.pop('video_contents', None)
        dynamic_content_data = validated_data.pop('dynamic_contents', None)

        # Create BaseContent instance
        base_content = BaseContent.objects.create(**validated_data)

        # Create associated VideoContent or DynamicContent if data is provided
        if video_content_data:
            VideoContent.objects.create(base_content=base_content, **video_content_data)
        elif dynamic_content_data:  # Ensure only one is created based on content_type
            DynamicContent.objects.create(base_content=base_content, **dynamic_content_data)

        return base_content

    def update(self, instance, validated_data):
        # Pop nested data for video_contents and dynamic_contents if provided
        video_content_data = validated_data.pop('video_contents', None)
        dynamic_content_data = validated_data.pop('dynamic_contents', None)

        # Update BaseContent instance
        instance = super().update(instance, validated_data)

        # Update or create VideoContent if data is provided
        if video_content_data:
            VideoContent.objects.update_or_create(
                base_content=instance, defaults=video_content_data
            )
        elif dynamic_content_data:  # Ensure only one is updated based on content_type
            DynamicContent.objects.update_or_create(
                base_content=instance, defaults=dynamic_content_data
            )

        return instance


# RevisionContent Serializer
class RevisionContentSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), source='topic', write_only=True
    )
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = RevisionContent
        fields = [
            'id', 'topic', 'topic_id', 'video_url', 
            'created_at', 'updated_at'
        ]
