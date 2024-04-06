from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

# create CRUD routes for every registered viewsets
router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, "user")

urlpatterns = [
    path("api/", include((router.urls, "users"), namespace="users")),
    path("api/", include(("api.urls", "api"), namespace="api")),
    path("admin/", admin.site.urls),
]
