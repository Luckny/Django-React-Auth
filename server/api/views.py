from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from .permissions import UserPermission

# from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from .serializers import UserSerializer, ObtainAuthTokenSerializer
from .models import User, EmailConfirmationToken
from .utils import send_confirmation_email
from django.shortcuts import get_object_or_404


# creating viewsets here. docs: https://www.django-rest-framework.org/
# https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create
class UserViewSet(viewsets.ModelViewSet):
    # will return all users including admins
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
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

        # create the email confirmation token
        email_token = EmailConfirmationToken.objects.create(user=user)

        try:
            # send email for confirmation
            send_confirmation_email(user.email, email_token.pk, user.pk)
        except Exception as e:  # pragma no cover
            # If sending email fails, delete the user and email_token
            user.delete()
            email_token.delete()

            print("Failed to send confirmation email:", e)  # debugging

            raise ValidationError("Failed to send confirmation email.")


# end point for confirming a user's email address
@api_view(["POST"])
def confirm_email_view(request, token_id, user_id):
    email_token = get_object_or_404(EmailConfirmationToken, pk=token_id)

    # get user from email_toek
    user = email_token.user

    # compare email_token's user with user_id from param
    if user.pk == user_id:
        user.is_active = True  # confirm email
        user.save()
        return Response({"message": "email confirmed succesfully"}, status=200)


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
