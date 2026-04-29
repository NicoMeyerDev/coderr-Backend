from django.contrib.auth.models import User
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import Profile

from ..filters import OfferFilter, ReviewFilter
from .pagination import CustomPagination
from .permissions import IsOfferBusinessUserOrReadOnly, IsOrderCustomerOrBusinessUser, IsReviewAuthorOrReadOnly
from .serializer import (BaseInfoSerializer,OfferCreateUpdateSerializer,OfferDetailListSerializer,OfferDetailSerializer,OfferIdSerializer,OfferSerializer,OfferSingleSerializer,OrderSerializer,ReviewSerializer,UserSerializer,)
from coderr_app.models import Offer, OfferDetail, Order, Review


class OfferView(generics.ListCreateAPIView):
    """
    Lists and creates offers with filtering, search, and ordering.
    Allows authenticated business users to create new offers.
    Supports pagination for large result sets.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at"]
    

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateUpdateSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        serializer.save(business_user=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsOfferBusinessUserOrReadOnly()]
        return [AllowAny()]


class OfferSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a single offer.
    Requires authentication and appropriate permissions.
    Supports partial updates for flexibility.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSingleSerializer
    permission_classes = [IsAuthenticated, IsOfferBusinessUserOrReadOnly]
    

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return OfferCreateUpdateSerializer
        return OfferIdSerializer
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        write_serializer = OfferCreateUpdateSerializer(instance=instance, data=request.data, partial=True)
        write_serializer.is_valid(raise_exception=True)
        write_serializer.save()
        read_serializer = OfferSingleSerializer(instance)   
        return Response(read_serializer.data, status=status.HTTP_200_OK)
    

class OfferDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieves and updates offer details.
    Allows business users to modify specific offer information.
    Ensures proper permissions are enforced.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, IsOfferBusinessUserOrReadOnly]
    lookup_field = "id"

    
class OrderView(generics.ListCreateAPIView):
    """
    Lists and creates orders based on offer details.
    Automatically populates order data from selected offers.
    Requires authentication for order creation.
    """
    queryset = Order.objects.all().order_by("created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderCustomerOrBusinessUser]
    pagination_class = None

    def perform_create(self, serializer):
        offer_detail_id = self.request.data.get("offer_detail_id")
        
        if not offer_detail_id:
            raise ValidationError({"offer_detail_id": "Dieses Feld ist erforderlich."})
        
        try:
            offer_detail_id = int(offer_detail_id)
        except (ValueError, TypeError):
                raise ValidationError({"offer_detail_id": "Ungültiger Wert."})
    
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
                raise NotFound({"offer_detail_id": "OfferDetail nicht gefunden."})  

        serializer.save(customer_user=self.request.user, business_user=offer_detail.offer.business_user, title=offer_detail.title, revisions=offer_detail.revisions, delivery_time_in_days=offer_detail.delivery_time_in_days, price=offer_detail.price, features=offer_detail.features, offer_type=offer_detail.offer_type)
       

class OrderSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a single order.
    Ensures only authorized users can modify orders.
    Supports full CRUD operations with validation.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderCustomerOrBusinessUser]
    

class BusinessOrderCountView(APIView):
    """Returns the count of in-progress orders for a business user."""
    permission_classes = [IsAuthenticated]
    

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")

        if not user_id:
            raise ValidationError({"user_id": "Dieses Feld ist erforderlich."})    
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound({"detail": "Benutzer nicht gefunden."})

        
        
        count = Order.objects.filter(business_user_id=user_id, status="in_progress").count()
        return Response({"order_count": count}) 

        
class CompletedOrderCountView(APIView):
    """Returns the count of completed orders for a business user."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        if not user_id:
            raise ValidationError({"user_id": "Dieses Feld ist erforderlich."})    
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound({"detail": "Benutzer nicht gefunden."})
        
        count = Order.objects.filter(business_user_id=user_id, status="completed").count()
        return Response({"completed_order_count": count})    


class ReviewView(generics.ListCreateAPIView):
    """
    Lists and creates reviews with validation.
    Prevents duplicate reviews from the same customer.
    Allows filtering and ordering of reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_class = ReviewFilter
    ordering_fields = ["updated_at", "rating"]


    def perform_create(self, serializer):
        business_user_id = self.request.data.get("business_user")

        if not business_user_id:
            raise ValidationError({"business_user": "Dieses Feld ist erforderlich."})

        business_user = get_object_or_404(User, id=business_user_id)

        if self.request.user.profile.type != "customer":
            raise PermissionDenied("Nur Kunden können Bewertungen erstellen.")

        already_reviewed = Review.objects.filter(
            reviewer=self.request.user,
            business_user=business_user
        ).exists()

        if already_reviewed:
            raise ValidationError({
                "detail": "Sie haben diesen Business-User bereits bewertet."
            })

        serializer.save(
            reviewer=self.request.user,
            business_user=business_user
        )

    
class ReviewSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a single review.
    Only the review author can modify their review.
    Enforces read-only access for others.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]    


class BaseInfoView(APIView):
    """
    Provides basic platform statistics.
    Includes review counts, average ratings, and user metrics.
    Accessible to all users without authentication.
    """
    permission_classes = [AllowAny]
    
   

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        average_rating = round(Review.objects.aggregate(average_rating=models.Avg("rating"))["average_rating"] or 0, 1)
        business_profile_count = Profile.objects.filter(type="business").count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

        serializer = BaseInfoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
  
    
        
