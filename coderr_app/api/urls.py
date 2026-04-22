from django.urls import path
from .views import CompletedOrderCountView, OfferView, OfferSingleView, OrderView, OrderSingleView, ReviewView, ReviewSingleView, BaseInfoView, OfferDetailView, BusinessOrderCountView

urlpatterns = [

    path("offers/", OfferView.as_view(), name="offer-list-create"),
    path("offers/<int:pk>/", OfferSingleView.as_view(), name="offer-detail"),
    path("offerdetails/<int:id>/", OfferDetailView.as_view(), name="offer-detail"),  # Neue URL für Angebotsdetails

    path("orders/", OrderView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderSingleView.as_view(), name="order-detail"),
    path("order-count/<int:user_id>/", BusinessOrderCountView.as_view(), name="business-order-count"),
    path("completed-order-count/<int:user_id>/", CompletedOrderCountView.as_view(), name="completed-order-count"),

    path("reviews/", ReviewView.as_view(), name="review-list-create"),
    path("reviews/<int:pk>/", ReviewSingleView.as_view(), name="review-detail"),

    path("base-info/", BaseInfoView.as_view(), name="base-info"),
]