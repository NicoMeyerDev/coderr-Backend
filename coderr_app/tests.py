from django.test import TestCase

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from auth_app.models import Profile
from coderr_app.models import Offer

class OfferTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/offers/'
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_data = Profile.objects.create(user=self.user, type='business')
        self.client.force_authenticate(user=self.user)
        self.offer = Offer.objects.create(
            business_user=self.user,
            title="Test Offer",
            description="This is a test offer.",
        )

    def test_get_offer(self):
        response = self.client.get(f'{self.url}')
        self.assertEqual(response.status_code, 200)
        

    def test_post_offer(self):
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
            "Logo Design",
            "Visitenkarte"
        ],
        "offer_type": "basic"
        },
        {
        "title": "Standard Design",
        "revisions": 5,
        "delivery_time_in_days": 7,
        "price": 200,
        "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
        ],
        "offer_type": "standard"
        },
        {
        "title": "Premium Design",
        "revisions": 10,
        "delivery_time_in_days": 10,
        "price": 500,
        "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
        ],
        "offer_type": "premium"
        }
        ]
    }   
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)    

    def test_post_offer_with_missing_details(self):
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)    

    def test_post_ofer_is_not_authenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
            "Logo Design",
            "Visitenkarte"
        ],
        "offer_type": "basic"
        },
        {
        "title": "Standard Design",
        "revisions": 5,
        "delivery_time_in_days": 7,
        "price": 200,
        "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
        ],
        "offer_type": "standard"
        },
        {
        "title": "Premium Design",
        "revisions": 10,
        "delivery_time_in_days": 10,
        "price": 500,
        "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
        ],
        "offer_type": "premium"
        }
    ]   
    }   
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 401)    

    def test_post_offer_is_not_business_user(self):
        self.user_data.type = 'customer'
        self.user_data.save()
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
            "Logo Design",
            "Visitenkarte"
        ],
        "offer_type": "basic"
        },
        {
        "title": "Standard Design",
        "revisions": 5,
        "delivery_time_in_days": 7,
        "price": 200,
        "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
        ],
        "offer_type": "standard"
        },
        {
        "title": "Premium Design",
        "revisions": 10,
        "delivery_time_in_days": 10,
        "price": 500,
        "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
        ],
        "offer_type": "premium"
        }
    ]   
    }   
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 403)    

class OfferDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_data = Profile.objects.create(user=self.user, type='business')
        self.client.force_authenticate(user=self.user)
        self.offer = Offer.objects.create(
            business_user=self.user,
            title="Test Offer",
            description="This is a test offer.",
        ) 
        self.offer_detail_url = f'/api/offers/{self.offer.id}/'
       
        
    def test_get_offer_id_successful(self):
        response = self.client.get(self.offer_detail_url)
        self.assertEqual(response.status_code, 200)

    def test_get_offer_is_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.offer_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_get_offer_not_found(self):
        response = self.client.get('/api/offers/999/')
        self.assertEqual(response.status_code, 404)
            
class PatchOfferTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_data = Profile.objects.create(user=self.user, type='business')
        self.client.force_authenticate(user=self.user)
        self.offer = Offer.objects.create(
            business_user=self.user,
            title="Test Offer",
            description="This is a test offer.",
        ) 
        self.offer_detail_url = f'/api/offers/{self.offer.id}/'
        
    def test_patch_offer_successful(self):
        data = {
                "title": "Updated Grafikdesign-Paket",
                "details": [
                {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
            "Logo Design",
            "Flyer"
            ],
            "offer_type": "basic"
        }
    ]
    }
        response = self.client.patch(self.offer_detail_url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_offer_is_not_authenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            "title": "Updated Test Offer",
            "description": "This is an updated test offer.",
        }
        response = self.client.patch(self.offer_detail_url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_patch_offer_not_found(self):
        data = {
            "title": "Updated Test Offer",
            "description": "This is an updated test offer.",
        }
        response = self.client.patch('/api/offers/999/', data, format='json')
        self.assertEqual(response.status_code, 404)          
       
class DeleteOfferIdTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_data = Profile.objects.create(user=self.user, type='business')
        self.client.force_authenticate(user=self.user)
        self.offer = Offer.objects.create(
            business_user=self.user,
            title="Test Offer",
            description="This is a test offer.",
        ) 
        self.offer_detail_url = f'/api/offers/{self.offer.id}/'
        
    def test_delete_offer_successful(self):
        response = self.client.delete(self.offer_detail_url)
        self.assertEqual(response.status_code, 204)

    def test_delete_offer_is_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.offer_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_delete_offer_is_authenticated_but_not_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.user_data = Profile.objects.create(user=other_user, type='business')
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(self.offer_detail_url)
        self.assertEqual(response.status_code, 403)    

    def test_delete_offer_not_found(self):
        response = self.client.delete('/api/offers/999/')
        self.assertEqual(response.status_code, 404)        

class OfferDetailIdTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_data = Profile.objects.create(user=self.user, type='business')
        self.client.force_authenticate(user=self.user)
        self.offer = Offer.objects.create(
            business_user=self.user,
            title="Test Offer",
            description="This is a test offer.",
        )
        self.offerdetail = self.offer.details.create(
            title="Basic Design",
            offer_type="basic",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"]
        )
        self.offer_detail_url = f'/api/offerdetails/{self.offerdetail.id}/'
        
    def test_get_offer_id_successful(self):
        response = self.client.get(self.offer_detail_url)
        self.assertEqual(response.status_code, 200)

    def test_get_offer_is_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.offer_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_get_offer_not_found(self):
        response = self.client.get('/api/offers/999/')
        self.assertEqual(response.status_code, 404)
     