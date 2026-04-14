from django.contrib import admin
from .models import Offer, OfferDetail, Order, Review


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

