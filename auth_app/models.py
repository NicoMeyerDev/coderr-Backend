from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLE_CHOICES = (
        ("customer", "Customer"),
        ("business_user", "Business User"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default="customer")

    def __str__(self):
        return f"{self.user.username} - {self.role}"

