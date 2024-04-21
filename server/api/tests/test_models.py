from rest_framework.test import APITestCase
from api.models import User
from api.models import OneTimePassword


class UserModelTest(APITestCase):
    default_email = "user@email.com"
    default_pass = "password1!"

    # add user with default email and default password to database
    def create_default_user(self):
        # user in database
        user = User.objects.create_user(
            email=self.default_email, password=self.default_pass
        )
        return user

    def test_otp_str(self):
        user = self.create_default_user()
        otp = OneTimePassword.objects.create(user=user)

        self.assertEqual(str(otp), otp.code)
