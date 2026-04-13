from django.contrib import admin
from auth_app.models import Profile, Offer, Order, Review

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]
    list_filter = ["role"]

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ["offer", "title", "offer_type", "price", "delivery_time_in_days", "revisions"]
    list_filter = ["offer_type", "delivery_time_in_days"]
    search_fields = ["title", "features"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
