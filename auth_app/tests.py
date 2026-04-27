from .models import Profile

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class RegistrationTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/registration/'

    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
            
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)

    def test_registration_with_mismatched_passwords(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword1',
            'type': 'customer'
        }
        response = self.client.post(self.url, data)     
        self.assertEqual(response.status_code, 400)

class LoginTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/login/'
        User.objects.create_user(username='testuser', password='testpassword')  
        
    def test_successful_login(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.url, self.user_data)    
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_credentials(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, self.user_data)    
        self.assertEqual(response.status_code, 400)

class ProfileTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = f'/api/profile/{self.user.id}/'
        self.user_data = Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_profile_successful(self):
        response = self.client.get(self.url)    
        self.assertEqual(response.status_code, 200)    

    def test_get_profile_unauthorized(self):
        self.client.force_authenticate(user=None)  
        response = self.client.get(self.url)    
        self.assertEqual(response.status_code, 401)

    def test_get_profile_not_found(self):
        self.url = '/api/profile/9999/'  
        response = self.client.get(self.url)    
        self.assertEqual(response.status_code, 404)   

    def test_patch_profile_successful(self):
        data = {
                "first_name": "Max",
                "last_name": "Mustermann",
                "location": "Berlin",
                "tel": "987654321",
                "description": "Updated business description",
                "working_hours": "10-18",
                "email": "new_email@business.de"
        }
        response = self.client.patch(self.url, data)    
        self.assertEqual(response.status_code, 200)         

    def test_patch_profile_unauthorized(self):
        self.client.force_authenticate(user=None)  
        data = {
                "first_name": "Max",
                "last_name": "Mustermann",
                "location": "Berlin",
                "tel": "987654321",
                "description": "Updated business description",
                "working_hours": "10-18",
                "email": "new_email@business.de"
        }
        response = self.client.patch(self.url, data)    
        self.assertEqual(response.status_code, 401)         

    def test_patch_user_is_not_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.force_authenticate(user=other_user)  
        data = {
                "first_name": "Max",
                "last_name": "Mustermann",
                "location": "Berlin",
                "tel": "987654321",
                "description": "Updated business description",
                "working_hours": "10-18",
                "email": "new_email@business.de"
        }
        response = self.client.patch(self.url, data)    
        self.assertEqual(response.status_code, 403)         

    def test_patch_profile_not_found(self):
        self.url = '/api/profile/9999/'  
        data = {
                "first_name": "Max",
                "last_name": "Mustermann",
                "location": "Berlin",
                "tel": "987654321",
                "description": "Updated business description",
                "working_hours": "10-18",
                "email": "new_email@business.de"
        }
        response = self.client.patch(self.url, data)    
        self.assertEqual(response.status_code, 404)         


    def test_get_profile_is_Business(self):
        self.user_data.type = "business"
        self.user_data.save()
        response = self.client.get(self.url)    
        self.assertEqual(response.status_code, 200)

    def test_get_profile_business_not_authenticated(self):
        self.client.force_authenticate(user=None)  
        response = self.client.get(self.url)    
        self.assertEqual(response.status_code, 401)    

    def test_get_profile_is_Customer(self):
        self.user_data.type = "customer"
        self.user_data.save()
        response = self.client.get(self.url)    
        self.assertEqual(response.status_code, 200)

    def test_get_profile_customer_not_authenticated(self):
        self.client.force_authenticate(user=None)  
        response = self.client.get(self.url)    
        self.assertEqual(response.status_code, 401)                 