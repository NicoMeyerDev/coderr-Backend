from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLE_CHOICES = (
        ("customer", "Customer"),
        ("business_user", "Business User"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default="customer")

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Offer(models.Model):
    #business user sein, der ein Angebot erstellt
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    
    #man sieht einen title
    title = models.CharField(max_length=200)
    
    #man sieht eine description
    description = models.TextField()
    
    
    #man sieht wann das Angebot erstellt wurde
    created_at = models.DateTimeField(auto_now_add=True)
    
    #man sieht wann das Angebot aktualisiert wurde
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.business_user.username}"
    

class OfferDetail(models.Model):
    # gehört zu einem Offer
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")

    # Paketname
    title = models.CharField(max_length=100)

    # Typ (basic, standard, premium)
    OFFER_TYPE_CHOICES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default="basic")

    # Leistung
    revisions = models.IntegerField(default=1)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Features
    features = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.offer.title} - {self.title} ({self.offer_type})"    

class Order(models.Model):
    pass

class Review(models.Model):
    pass