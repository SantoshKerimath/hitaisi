from django.urls import path
from .views import ClaimCreateView, ClaimListView

urlpatterns = [
    path('create/', ClaimCreateView.as_view()),
    path('', ClaimListView.as_view()),
]
