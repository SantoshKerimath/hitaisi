from os import name
from django.urls import path
from .views import OrganizationCreateView, UserCreateView, MeView

urlpatterns = [
    path('orgs/', OrganizationCreateView.as_view(), name="create-org"),
    path('users/', UserCreateView.as_view(), name="create-user"),
    path('auth/me/', MeView.as_view(), name="user-view"),
]
