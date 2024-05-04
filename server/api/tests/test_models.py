import datetime
from django.utils import timezone
from django.test.utils import tag
from django.test import TestCase
from api.models import User, OneTimePassword, five_minutes


class UserTestCase(TestCase):
    valid_email = "valid@email.com"
    valid_password = "secret123"

    def setUp(self):
        method = getattr(self, self._testMethodName)
        tags = getattr(method, "tags", {})
        if "skip_setup" in tags:
            return  # setUp skipped

    @tag("skip_setup")
    def test_create_user_valid(self):
        User.objects.create_user(email=self.valid_email, password=self.valid_password)

        # user should exist in db
        user = User.objects.filter(email=self.valid_email).first()
        self.assertIsNotNone(user)

    def test_create_user_missing_required_fields(self):
        # no email should raise value error
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password=self.valid_password)

        # no password should raise value error
        with self.assertRaises(ValueError):
            User.objects.create_user(email=self.valid_email, password=None)

    def test_create_super_user_working(self):
        User.objects.create_superuser(
            email=self.valid_email, password=self.valid_password
        )

        # filter returns a list of users
        user = User.objects.filter(email=self.valid_email).first()
        # should be defined
        self.assertIsNotNone(user)
        # should be super user
        self.assertTrue(user.is_superuser)
        # should have staff privilege
        self.assertTrue(user.is_staff)

    def test_add_five_minutes(self):
        expected_time = timezone.localtime(timezone.now()) + datetime.timedelta(
            minutes=5
        )
        result = five_minutes()
        self.assertAlmostEqual(
            result, expected_time, delta=datetime.timedelta(seconds=1)
        )


# class OneTimePassword(models.Model):
#     # random unique field of 6 characters
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     code = models.CharField(max_length=6, default=secrets.token_hex(3).upper())
#     # related user
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # OTP expires after 5 minutes of creation
#     expires_at = models.DateTimeField(default=five_minutes)
#
#     def __str__(self) -> str:
#         return f"{self.code}"
class OneTimePasswordTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="valid@email.com", password="secret123"
        )

    def test_create_otp(self):
        otp = OneTimePassword.objects.create(user=self.user)
        self.assertIsNotNone(otp)
        self.assertEqual(otp.user, self.user)
        # should have length of 6 characters
        self.assertEqual(len(otp.code), 6)

    def test_otp_string_representation(self):
        # Create an OTP instance
        otp = OneTimePassword.objects.create(user=self.user)

        # Check if __str__ method returns the code
        self.assertEqual(str(otp), otp.code)
