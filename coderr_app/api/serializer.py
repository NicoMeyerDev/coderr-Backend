from rest_framework import serializers
from django.contrib.auth.models import User
from coderr_app.models import Offer, OfferDetail, Order, Review
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    
    def get_fullname(self, obj):
        return obj.get_full_name() or obj.username
    

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
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]


class OfferSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="business_user.id", read_only=True)
    details = OfferDetailListSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time", "user_details"]

    
    def validate_title(self, title):
        title = title.strip()
        if not title:
            raise serializers.ValidationError("Titel darf nicht leer sein")
        return title 
    
    def get_details(self, obj):
        details = obj.details.all()
        return OfferDetailListSerializer(details, many=True).data

    def get_min_price(self, obj):
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        times = obj.details.values_list("delivery_time_in_days", flat=True)  # Annahme: Feld 'delivery_time' in OfferDetail
        return min(times) if times else None
    
    def get_user_details(self, obj):
        return OfferUserDetailsSerializer(obj.business_user).data
    
    def create(self, validated_data):
        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer


class OfferIdSerializer(OfferSerializer):
    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time"]


class OfferSingleSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
   

    class Meta:
        model = Offer
        fields = ["id","title", "image", "description", "details"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['details'] = sorted(rep['details'], key=lambda x: x['id'])
        return rep
    
class OfferCreateUpdateSerializer(serializers.ModelSerializer): #
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def create(self, validated_data):
        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", [])
        instance.title = validated_data.get("title", instance.title)
        instance.image = validated_data.get("image", instance.image)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        # Details aktualisieren
        for detail_data in details_data:
            offer_type = detail_data.get("offer_type")
           
            try:
                detail = OfferDetail.objects.get(offer=instance, offer_type=offer_type)
                detail.title = detail_data.get("title", detail.title)
                detail.revisions = detail_data.get("revisions", detail.revisions)
                detail.price = detail_data.get("price", detail.price)
                detail.delivery_time_in_days = detail_data.get("delivery_time_in_days", detail.delivery_time_in_days)
                detail.features = detail_data.get("features", detail.features)
                detail.save()
            except OfferDetail.DoesNotExist:
                raise ValidationError({"offer_type": f"Kein Detail mit offer_type '{offer_type}' gefunden."})

        return instance
    
    def validate_details(self, value):
        if self.instance is None and len(value) < 3:
            raise serializers.ValidationError("Ein Angebot muss mindestens 3 Details enthalten.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.IntegerField(source="customer_user.id", read_only=True)
    business_user = serializers.IntegerField(source="business_user.id", read_only=True)
    title = serializers.CharField(read_only=True)
    delivery_time_in_days = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = Order
        fields = ["id", "customer_user", "business_user",  "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"]    


class OrderdetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"] 


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    reviewer = serializers.IntegerField(source="reviewer.id", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]


class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()

    class Meta:
        fields = ["review_count", "average_rating", "business_profile_count", "offer_count"]