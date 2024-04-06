from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User, EmailConfirmationToken
from .utils import send_confirmation_email
from django.shortcuts import get_object_or_404


# creating viewsets here. docs: https://www.django-rest-framework.org/
# https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create
class UserViewSet(viewsets.ModelViewSet):
    # will return all users including admins
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # overing saving method
    def perform_create(self, serializer):
        # save the user
        user = serializer.save()

        # create the email confirmation token
        token = EmailConfirmationToken.objects.create(user=user)

        try:
            # send email for confirmation
            send_confirmation_email(user.email, token.pk, user.pk)
        except Exception as e:  # pragma no cover
            # If sending email fails, delete the user and token
            user.delete()
            token.delete()

            print("Failed to send confirmation email:", e)  # debugging

            raise ValidationError("Failed to send confirmation email.")


@api_view(["POST"])
def confirm_email_view(request, token_id, user_id):
    token = get_object_or_404(EmailConfirmationToken, pk=token_id)

    # get user from token
    user = token.user

    # compare token's user with user_id from param
    if user.pk == user_id:
        user.is_email_confirmed = True  # confirm email
        user.save()
        return Response({"message": "email confirmed succesfully"}, status=200)
