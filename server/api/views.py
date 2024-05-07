from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .permissions import UserPermission
from .authentication import CustomTokenAuth
from django.utils import timezone
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    ObtainAuthTokenSerializer,
    OneTimePasswordSerializer,
)
from .models import User, OneTimePassword
from .utils import send_confirmation_email
from django.shortcuts import get_object_or_404


# creating viewsets here. docs: https://www.django-rest-framework.org/
# https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create
class UserViewSet(viewsets.ModelViewSet):
    # will return all users including admins
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (CustomTokenAuth,)
    permission_classes = (UserPermission,)

    # overriden create method for login user token management
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        access_token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response(
            data={"user": serializer.data, "access_token": access_token.key},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    # overriding saving method
    def perform_create(self, serializer):
        # save the user
        user = serializer.save()

        # create the one time password for the user
        otp = OneTimePassword.objects.create(user=user)

        try:
            # send email for confirmation
            send_confirmation_email(user.email, otp.code)
        except Exception:  # pragma no cover
            # If sending email fails, delete the user and otp
            user.delete()
            otp.delete()

            raise ValidationError("Failed to send confirmation email.")


class ConfirmEmailAPIView(APIView):
    def post(self, request):
        otp_serializer = OneTimePasswordSerializer(data=request.data)
        if otp_serializer.is_valid():
            code = otp_serializer.data["code"]

            otp = get_object_or_404(OneTimePassword, code=code)

            # get user from onetimepassword
            user = otp.user
            # if otp not expired yet
            if timezone.localtime(otp.expires_at) >= timezone.localtime(timezone.now()):
                user.is_active = True  # activate user account
                user.save()
                return Response({"message": "email confirmed succesfully"}, status=200)
            else:
                raise ValueError("one time password expired")
        return Response({"message": otp_serializer.errors}, status=500)


# custum class for login and token
class ObtainAuthToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = ObtainAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            data={
                "user": ObtainAuthTokenSerializer(user).data,
                "access_token": token.key,
            },
            status=status.HTTP_200_OK,
        )
