from django.urls import path
from .views import confirm_email_view, ObtainAuthToken


urlpatterns = [
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("confirm/<uuid:token_id>/<uuid:user_id>", confirm_email_view, name="confirm"),
]
