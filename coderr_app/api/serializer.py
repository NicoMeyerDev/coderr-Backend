from rest_framework import serializers
from django.contrib.auth.models import User
from coderr_app.models import Offer, OfferDetail, Order, Review


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    
    def get_fullname(self, obj):
        return obj.get_full_name() or obj.username
    

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="business_user.id", read_only=True)
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "description", "image", "created_at", "updated_at", "details", "min_price", "min_delivery_time", "user_details"]

    
    def validate_title(self, title):
        title = title.strip()
        if not title:
            raise serializers.ValidationError("Titel darf nicht leer sein")
        return title 
    
    def get_details(self, obj):
        details = obj.details.all()
        return OfferDetailSerializer(details, many=True).data
    
    def get_min_price(self, obj):
        # Berechnet den minimalen Preis aus den Details
        prices = obj.details.values_list("price", flat=True)  # Annahme: Feld 'price' in OfferDetail
        return min(prices) if prices else None
    
    def get_min_delivery_time(self, obj):
        # Berechnet die minimale Lieferzeit aus den Details
        times = obj.details.values_list("delivery_time_in_days", flat=True)  # Annahme: Feld 'delivery_time' in OfferDetail
        return min(times) if times else None
    
    def get_user_details(self, obj):
        # Gibt Benutzerdetails zurück
        return OfferUserDetailsSerializer(obj.business_user).data


class OfferUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferDetailListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ["id", "offer", "title", "offer_type", "revisions", "delivery_time_in_days", "price", "features"]


class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.IntegerField(source="customer_user.id", read_only=True)
    business_user = serializers.IntegerField(source="business_user.id", read_only=True)
    customer_username = serializers.CharField(source="customer_user.username", read_only=True)
    business_username = serializers.CharField(source="business_user.username", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_user", "customer_username", "business_user", "business_username", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"]    


class OrderdetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"] 


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]

class BaseInfoSerializer(serializers.Serializer):
    total_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()
    total_business_users = serializers.IntegerField()
    total_offers = serializers.IntegerField()

    class Meta:
        fields = ["total_reviews", "average_rating", "total_business_users", "total_offers"]