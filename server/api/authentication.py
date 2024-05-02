from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


class CustomTokenAuth(TokenAuthentication):

    # removed is_active validation

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token.")

        return (token.user, token)
