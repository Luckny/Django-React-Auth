from django.urls import reverse
from rest_framework.test import APITestCase
from api.models import User

class UsersAPITests(APITestCase):
    default_test_email = 'user@email.com'
    default_test_password = 'password1!'
    
    def test_signup_working(self):
        url = reverse('users:user-list')
        body = {'email': self.default_test_email, 'password': self.default_test_password} # user creation body
        response = self.client.post(url, body, format='json')
        # reponse should have status code of 201 (creation)
        self.assertEqual(response.status_code, 201)
        # filter returns a list of users
        user = User.objects.filter(email=body['email']).first()
        # should be defined
        self.assertIsNotNone(user)
        # check password built in function. asserting equal would fail because of hashing
        self.assertTrue(user.check_password(body['password']))
        
    def test_signup_no_double_emails(self):
        # user in database
        user = User.objects.create_user(email=self.default_test_email, password=self.default_test_password)
        
        url = reverse('users:user-list')
        #creating a user with the same email
        body = {'email': self.default_test_email, 'password': self.default_test_password} # user creation body
        response = self.client.post(url, body, format='json')
        # reponse should have status code of 400 (bad request)
        self.assertEqual(response.status_code, 400)
        
    def test_login_working(self):
        # user in database
        user = User.objects.create_user(email=self.default_test_email, password=self.default_test_password)
        
        url = reverse('api:login')
        body = {'username': self.default_test_email, 'password': self.default_test_password}
        response = self.client.post(url, body, format='json')
        # reponse should have status code of 200 (ok)
        self.assertEqual(response.status_code, 200)
        # response should have a token
        self.assertIn('token', response.data)
    
    def test_login_bad_password(self):
        #user in database
        user = User.objects.create_user(email=self.default_test_email, password=self.default_test_password)
        
        url = reverse('api:login')
        body = {'username': self.default_test_email, 'password': 'badPassword'}
        response = self.client.post(url, body, format='json')
        # reponse should have status code of 400 (Bad request)
        self.assertEqual(response.status_code, 400)    
