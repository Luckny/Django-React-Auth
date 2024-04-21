from django.urls import path
from .views import ConfirmEmailAPIView, ObtainAuthToken


urlpatterns = [
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("confirm_email/", ConfirmEmailAPIView.as_view(), name="confirm"),
]
