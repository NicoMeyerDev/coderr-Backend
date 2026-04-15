from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ("customer", "Customer"),
        ("business_user", "Business User"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    file = models.FileField(upload_to="profile_files/", null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="customer")
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.user.username} - {self.type}"

