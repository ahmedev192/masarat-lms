from django.contrib.auth.models import User
from django.db import models

# Enum choices for the academic year, learning type, and major
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

class Major(models.TextChoices):
    SCIENCE = 'Science', 'Science'
    ARTS = 'Arts', 'Arts'
    COMMERCE = 'Commerce', 'Commerce'
    ENGINEERING = 'Engineering', 'Engineering'

class Parent(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store password securely
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email



class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    academic_year = models.CharField(max_length=20, choices=AcademicYear.choices)
    parent = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True, blank=True)
    learning_type = models.CharField(max_length=20, choices=LearningType.choices)
    first_time_login = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    major = models.CharField(max_length=20, choices=Major.choices, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
