from rest_framework.permissions import BasePermission, SAFE_METHODS
from coderr_app.models import Offer, Order, Review


# Angebot: alle d�rfen lesen, nur business_user darf �ndern und l�schen
class IsOfferBusinessUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.business_user == request.user


# Bestellung: Kunde darf erstellen/�ndern/l�schen, Business User darf sehen
class IsOrderCustomerOrBusinessUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.customer_user == request.user or obj.business_user == request.user
        if request.method in ("PATCH", "PUT", "DELETE"):
            return obj.customer_user == request.user
        return False


# Review: alle d�rfen lesen, nur reviewer darf �ndern/l�schen
class IsReviewAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user
