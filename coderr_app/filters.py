from django.db.models import Min
from django_filters import rest_framework as filters
from .models import Offer
from .models import Review

class OfferFilter(filters.FilterSet):
    """Filters offers by creator, minimum price, and maximum delivery time."""
    creator_id = filters.NumberFilter(field_name="business_user_id")
    min_price = filters.NumberFilter(method="filter_min_price")
    max_delivery_time = filters.NumberFilter(method="filter_max_delivery_time")

    class Meta:
        model = Offer
        fields = ["creator_id", "min_price", "max_delivery_time"]

    def filter_min_price(self, queryset, name, value):
        return queryset.annotate(
            lowest_price=Min("details__price")
        ).filter(lowest_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.annotate(
            lowest_delivery_time=Min("details__delivery_time_in_days")
        ).filter(lowest_delivery_time__lte=value)
    




class ReviewFilter(filters.FilterSet):
    """Filters reviews by business user and reviewer."""
    class Meta:
        model = Review
        fields = {
            "business_user": ["exact"],
            "reviewer": ["exact"],
        }    