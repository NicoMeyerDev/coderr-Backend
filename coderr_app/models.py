from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.business_user.username}"
    

class OfferDetail(models.Model):
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=100)

    OFFER_TYPE_CHOICES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default="basic")

    revisions = models.IntegerField(default=1)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.offer.title} - {self.title} ({self.offer_type})"    

class Order(models.Model):
    pass

class Review(models.Model):
    pass
