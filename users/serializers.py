from django.contrib.auth.models import User
from rest_framework import serializers
from .models import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "academic_year",
            "parent",
            "learning_type",
            "first_time_login",
            "phone_number",
            "gender",
            "date_of_birth",
            "profile_picture",  # Ensure that profile_picture is included
            "major",
        ]
        
    def update(self, instance, validated_data):
        # Allow updating the profile picture
        instance.academic_year = validated_data.get("academic_year", instance.academic_year)
        instance.parent = validated_data.get("parent", instance.parent)
        instance.learning_type = validated_data.get("learning_type", instance.learning_type)
        instance.first_time_login = validated_data.get("first_time_login", instance.first_time_login)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)

        # Check if a new profile picture is provided
        profile_picture = validated_data.get("profile_picture", None)
        if profile_picture:
            instance.profile_picture = profile_picture  # Update the profile picture

        instance.major = validated_data.get("major", instance.major)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "student_profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Extract the nested student profile data
        student_profile_data = validated_data.pop("student_profile")
        
        # Create the user
        user = User.objects.create_user(**validated_data)
        
        # Create the associated student profile
        StudentProfile.objects.create(user=user, **student_profile_data)
        
        return user

    def update(self, instance, validated_data):
        # Update the user instance
        student_profile_data = validated_data.pop("student_profile", None)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()

        # Update the student profile instance
        if student_profile_data:
            student_profile = instance.student_profile
            for attr, value in student_profile_data.items():
                setattr(student_profile, attr, value)
            student_profile.save()
        
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ["username", "password", "email", "student_profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Extract the nested student profile data
        student_profile_data = validated_data.pop("student_profile")
        
        # Create the user
        user = User.objects.create_user(**validated_data)
        
        # Create the associated student profile
        StudentProfile.objects.create(user=user, **student_profile_data)
        
        return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Ensure that a user with this email exists
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Ensure that the new password and confirm password match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        # Ensure that the old password is correct
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        # Ensure that the old password and new password are different
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password cannot be the same as the old password.")
        return data
