from django.urls import path
from .views import OfferView, OfferSingleView, OrderView, OrderSingleView, ReviewView

urlpatterns = [

    
    path("offers/", OfferView.as_view(), name="offer-list-create"),
    path("offers/<int:pk>/", OfferSingleView.as_view(), name="offer-detail"),
    path("orders/", OrderView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderSingleView.as_view(), name="order-detail"),
    path("reviews/", ReviewView.as_view(), name="review-list-create"),

]