from django.urls import reverse
from rest_framework.test import APITestCase
from api.models import User, EmailConfirmationToken


class UsersAPITests(APITestCase):
    default_email = "user@email.com"
    default_pass = "password1!"

    # add user with default email and default password to database
    def create_default_user(self):
        # user in database
        user = User.objects.create_user(
            email=self.default_email, password=self.default_pass
        )
        return user

    # add user with default email and default password to database using api route
    def register_default_user(self):
        url = reverse("users:user-list")
        body = {
            "email": self.default_email,
            "password": self.default_pass,
        }  # user creation body
        response = self.client.post(url, body, format="json")
        return response

    def test_signup_working(self):
        response = self.register_default_user()
        # reponse should have status code of 201 (creation)
        self.assertEqual(response.status_code, 201)
        # filter returns a list of users
        user = User.objects.filter(email=self.default_email).first()
        # should be defined
        self.assertIsNotNone(user)
        # check password built in function.
        # Asserting equal would fail because of hashing
        self.assertTrue(user.check_password(self.default_pass))

    def test_signup_no_email(self):
        # creating a user with no email will raise a value error
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password=self.default_pass)

    def test_signup_no_double_emails(self):
        self.create_default_user()
        # creating user with the same email
        response = self.register_default_user()
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
        self.create_default_user()

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
        self.create_default_user()

        url = reverse("api:login")
        body = {"username": self.default_email, "password": "badPassword"}
        response = self.client.post(url, body, format="json")
        # reponse should have status code of 400 (Bad request)
        self.assertEqual(response.status_code, 400)

    def test_email_confirmation(self):
        # register user
        self.register_default_user()

        # get the new user
        user = User.objects.filter(email=self.default_email).first()

        # user's token should exist
        token = EmailConfirmationToken.objects.filter(user=user).first()
        self.assertIsNotNone(token)

        # user email should not be verified
        self.assertFalse(user.is_email_confirmed)

        url = reverse("api:confirm", args=[token.pk, user.pk])
        body = {"token_id": token.pk, "user_id": user.pk}
        # should validate email
        response = self.client.post(url, body, format="json")
        self.assertEqual(response.status_code, 200)

        # response is_email_confirmed should be true
        user.refresh_from_db()
        self.assertTrue(user.is_email_confirmed)
