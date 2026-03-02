from os import name
from django.urls import path
from .views import ClaimCreateView, ClaimListView

urlpatterns = [
    path('create/', ClaimCreateView.as_view(), name="create-claim"),
    path('', ClaimListView.as_view(), name="claim-list"),
]
