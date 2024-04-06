from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import confirm_email_view


urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("confirm/<uuid:token_id>/<uuid:user_id>", confirm_email_view, name="confirm"),
]
