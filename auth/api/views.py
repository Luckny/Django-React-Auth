from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User, EmailConfirmationToken
from .utils import send_confirmation_email
from django.shortcuts import get_object_or_404, redirect


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

        # send email
        send_confirmation_email(email=user.email, token_id=token.pk, user_id=user.pk)


@api_view(["GET", "POST"])
def confirm_email_view(request, token_id, user_id):
    # verifying email
    if request.method == "POST":
        token = get_object_or_404(EmailConfirmationToken, pk=token_id)

        # compare token's user with recieved user_id
        user = token.user
        if user.pk == user_id:
            user.is_email_confirmed = True
            user.save()
            return redirect("users:user-detail", pk=user.pk)

    # get request
    return Response({"token_id": token_id, "user_id": user_id})
