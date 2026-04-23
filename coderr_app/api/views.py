from auth_app.models import Profile

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from django.contrib.auth.models import User
from django.db import models

from auth_app.api import serializer
from coderr_app.api.permissions import  IsOfferBusinessUserOrReadOnly, IsOrderCustomerOrBusinessUser, IsReviewAuthorOrReadOnly
from coderr_app.models import Offer, OfferDetail, Order, Review
from coderr_app.api.serializer import OfferCreateUpdateSerializer, OfferDetailSerializer, OfferSingleSerializer, UserSerializer, OfferSerializer, OfferDetailListSerializer, OrderSerializer, ReviewSerializer, BaseInfoSerializer



class OfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsOfferBusinessUserOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateUpdateSerializer
        return OfferSerializer

    def get_queryset(self):
        queryset = Offer.objects.all()

        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")
        ordering = self.request.query_params.get("ordering")
        search = self.request.query_params.get("search")

        if creator_id:
            try:
                creator_id = int(creator_id)    
            except ValueError:
                raise ValidationError({"creator_id": "Ungültiger Wert."})

            queryset = queryset.filter(business_user_id=creator_id)

        if min_price:
            try:
                min_price = float(min_price)
            except ValueError:
                raise ValidationError({"min_price": "Ungültiger Wert."})
            
            queryset = queryset.filter(details__price__gte=min_price)

        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
            except ValueError:
                raise ValidationError({"max_delivery_time": "Ungültiger Wert."})

            queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time)

        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search)
            )

        if ordering in ("updated_at", "-updated_at"):
            queryset = queryset.order_by(ordering)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(business_user=self.request.user)




class OfferSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSingleSerializer
    permission_classes = [IsAuthenticated, IsOfferBusinessUserOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return OfferCreateUpdateSerializer
        return OfferSingleSerializer


class OfferDetailView(generics.RetrieveUpdateAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated, IsOfferBusinessUserOrReadOnly]
    lookup_field = "id"

    
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
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

        serializer.save(customer_user=self.request.user, business_user=offer_detail.offer.business_user, title=offer_detail.offer.title, revisions=offer_detail.revisions, delivery_time_in_days=offer_detail.delivery_time_in_days, price=offer_detail.price, features=offer_detail.features, offer_type=offer_detail.offer_type)
       

class OrderSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderCustomerOrBusinessUser]
    

class BusinessOrderCountView(APIView):
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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated] #IsReviewAuthorOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        business_user_id = self.request.query_params.get("business_user_id")
        reviewer_id = self.request.query_params.get("reviewer_id")
        ordering = self.request.query_params.get("ordering")

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        if ordering in ("updated_at", "-updated_at", "rating", "-rating"):
            queryset = queryset.order_by(ordering)

        return queryset
    
    def perform_create(self, serializer):
        business_user = self.request.data.get("business_user")
        business_user = User.objects.get(id=business_user)
        
        already_reviewed = Review.objects.filter(reviewer=self.request.user, business_user=business_user).exists()
        print(already_reviewed, self.request.user, business_user)
        if already_reviewed:
            raise ValidationError({"detail": "Sie haben diesen Business bereits bewertet."})
        serializer.save(reviewer=self.request.user, business_user=business_user)

    
class ReviewSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]    


class BaseInfoView(APIView):   
    permission_classes = [IsAuthenticated]
    
   

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(average_rating=models.Avg("rating"))["average_rating"] or 0
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
    
  
    
        
