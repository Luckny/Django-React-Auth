"""
Serializers allow complex data such as model instances to be converted to
native Python datatypes that can then be easily rendered into JSON.
Serializers also provide deserialization, allowing parsed data to be converted
back into complex types, after first validating the incoming data.
source: https://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user

    class Meta:
        model = User
        fields = ["id", "email", "password", "is_email_confirmed"]