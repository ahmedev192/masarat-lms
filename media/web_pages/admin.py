from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User  # Import the User model
from .models import StudentProfile, Parent  # Import multiple models

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profiles'

class CustomUserAdmin(UserAdmin):
    inlines = (StudentProfileInline,)

# Unregister the default User admin
admin.site.unregister(User)
# Register the custom User admin
admin.site.register(User, CustomUserAdmin)

# Register your models with the admin site
admin.site.register(StudentProfile)
admin.site.register(Parent)
