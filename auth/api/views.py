from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth.models import User


# creating viewsets here. docs: https://www.django-rest-framework.org/
class UserViewSet(viewsets.ModelViewSet):
    # will return all users including admins
    queryset = User.objects.all()
    serializer_class = UserSerializer