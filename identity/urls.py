from django.urls import path
from .views import OrganizationCreateView, UserCreateView, MeView

urlpatterns = [
    path('orgs/', OrganizationCreateView.as_view()),
    path('users/', UserCreateView.as_view()),
    path('auth/me/', MeView.as_view()),
]
