"""
Serializers allow complex data such as model instances to be converted to
native Python datatypes that can then be easily rendered into JSON.
Serializers also provide deserialization, allowing parsed data to be converted
back into complex types, after first validating the incoming data.
source: https://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework import serializers
from .models import User, OneTimePassword
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.UUIDField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="user already exist")
        ]
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ["id", "email", "password", "is_active"]


class OneTimePasswordSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = OneTimePassword
        fields = ["code"]


class ObtainAuthTokenSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:  # valid credentials
            user = User.objects.filter(email=email).first()
            # if user exist
            if user:
                # valid password
                if user.check_password(password):
                    attrs["user"] = user
                    return attrs
                else:
                    raise ValidationError(
                        "unable to log in with provided credentials", code=401
                    )
            else:
                raise ValidationError("user not found", code=404)

        else:  # invalid credentials
            raise ValidationError("must include email and password")

    class Meta:
        model = User
        fields = ["id", "email", "password", "is_active"]
