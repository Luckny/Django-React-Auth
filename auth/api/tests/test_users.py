from django.urls import reverse
from rest_framework.test import APITestCase
from api.models import User


class UsersAPITests(APITestCase):
    default_email = "user@email.com"
    default_pass = "password1!"

    def test_signup_working(self):
        url = reverse("users:user-list")
        body = {
            "email": self.default_email,
            "password": self.default_pass,
        }  # user creation body
        response = self.client.post(url, body, format="json")
        # reponse should have status code of 201 (creation)
        self.assertEqual(response.status_code, 201)
        # filter returns a list of users
        user = User.objects.filter(email=body["email"]).first()
        # should be defined
        self.assertIsNotNone(user)
        # check password built in function.
        # Asserting equal would fail because of hashing
        self.assertTrue(user.check_password(body["password"]))

    def test_signup_no_email(self):
        # creating a user with no email will raise a value error
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password=self.default_pass)

    def test_signup_no_double_emails(self):
        # user in database
        _ = User.objects.create_user(
            email=self.default_email, password=self.default_pass
        )

        url = reverse("users:user-list")
        # creating a user with the same email
        body = {
            "email": self.default_email,
            "password": self.default_pass,
        }  # user creation body
        response = self.client.post(url, body, format="json")
        # reponse should have status code of 400 (bad request)
        self.assertEqual(response.status_code, 400)

    def test_create_super_user_working(self):
        user = User.objects.create_superuser(
            email=self.default_email, password=self.default_pass
        )

        # filter returns a list of users
        user = User.objects.filter(email=self.default_email).first()
        # should be defined
        self.assertIsNotNone(user)
        # should be super user
        self.assertTrue(user.is_superuser)
        # should have staff privilege
        self.assertTrue(user.is_staff)
        # check password built in function.
        # Asserting equal would fail because of hashing
        self.assertTrue(user.check_password(self.default_pass))

    def test_login_working(self):
        # user in database
        _ = User.objects.create_user(
            email=self.default_email, password=self.default_pass
        )

        url = reverse("api:login")
        body = {
            "username": self.default_email,
            "password": self.default_pass,
        }
        response = self.client.post(url, body, format="json")
        # reponse should have status code of 200 (ok)
        self.assertEqual(response.status_code, 200)
        # response should have a token
        self.assertIn("token", response.data)

    def test_login_bad_password(self):
        # user in database
        _ = User.objects.create_user(
            email=self.default_email, password=self.default_pass
        )

        url = reverse("api:login")
        body = {"username": self.default_email, "password": "badPassword"}
        response = self.client.post(url, body, format="json")
        # reponse should have status code of 400 (Bad request)
        self.assertEqual(response.status_code, 400)
