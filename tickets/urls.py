from os import name
from django.urls import path
from .views import CreateTicketView, AssignedTicketsView, AddTicketMessageView, UpdateTicketStatusView

urlpatterns = [
    path('create/', CreateTicketView.as_view(), name="create-ticket"),
    path('assigned/', AssignedTicketsView.as_view(), name="ticket-assigned"),
    path('message/add/', AddTicketMessageView.as_view(), name="ticket-message"),
    path("status/<int:pk>/", UpdateTicketStatusView.as_view(), name="ticket-status"),
]
