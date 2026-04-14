from django.contrib import admin
from auth_app.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]
    list_filter = ["role"]

