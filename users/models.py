from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    college_email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    has_voted = models.BooleanField(default=False)
    
    # Add these new fields for OTP functionality
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.student_id})"
