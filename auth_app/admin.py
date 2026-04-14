from django.contrib import admin
from auth_app.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "type"]
    list_filter = ["type"]

