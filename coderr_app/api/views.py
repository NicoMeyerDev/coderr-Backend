from cProfile import Profile

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db import models

from auth_app.api import serializer
from coderr_app.api.permissions import IsOfferBusinessUserOrReadOnly, IsOrderCustomerOrBusinessUser, IsReviewAuthorOrReadOnly
from coderr_app.models import Offer, OfferDetail, Order, Review
from coderr_app.api.serializer import OfferDetailSerializer, UserSerializer, OfferSerializer, OfferDetailListSerializer, OrderSerializer, ReviewSerializer, BaseInfoSerializer



class OfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsOfferBusinessUserOrReadOnly]

    def get_queryset(self):
        queryset = Offer.objects.all()

        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")
        ordering = self.request.query_params.get("ordering")
        search = self.request.query_params.get("search")

        if creator_id:
            queryset = queryset.filter(business_user_id=creator_id)

        if min_price:
            queryset = queryset.filter(offer_details__price__gte=min_price)

        if max_delivery_time:
            queryset = queryset.filter(offer_details__delivery_time_in_days__lte=max_delivery_time)

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
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsOfferBusinessUserOrReadOnly]


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderCustomerOrBusinessUser]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)


class OrderSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderCustomerOrBusinessUser]
    

class BusinessOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        count = Order.objects.filter(business_user=user, status="in_progress").count()
        return Response({"in_progress_order_count": count}) 


class CompletedOrderCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        count = Order.objects.filter(business_user=user, status="completed").count()
        return Response({"completed_order_count": count})    


class ReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated] #IsReviewAuthorOrReadOnly]

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
    
class ReviewSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]    
   
class BaseInfoView(APIView):   
    permission_classes = [IsAuthenticated]
    
   

    def get(self, request, *args, **kwargs):
        total_reviews = Review.objects.count()
        average_rating = Review.objects.aggregate(average_rating=models.Avg("rating"))["average_rating"] or 0
        total_business_users = Profile.objects.filter(is_business_user=True).count()
        total_offers = Offer.objects.count()

        data = {
            "total_reviews": total_reviews,
            "average_rating": average_rating,
            "total_business_users": total_business_users,
            "total_offers": total_offers,
        }

        serializer = BaseInfoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
  
    
        
