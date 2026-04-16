from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coderr_app.models import Offer, OfferDetail, Order, Review
from coderr_app.api.serializer import (
    OfferDetailSerializer,
    UserSerializer,
    OfferSerializer,
    OfferDetailListSerializer,
    OrderSerializer,
    ReviewSerializer,
)



class OfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(business_user=self.request.user)


class OfferSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #permission_classes = [IsAuthenticated, IsOfferMemberOrOwner]


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)


class OrderSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    #permission_classes = [IsAuthenticated]
    

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
    #permission_classes = [IsAuthenticated]

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
   

