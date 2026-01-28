from django.urls import path
from .views import CreateTicketView, AssignedTicketsView, AddTicketMessageView

urlpatterns = [
    path('create/', CreateTicketView.as_view()),
    path('assigned/', AssignedTicketsView.as_view()),
    path('message/add/', AddTicketMessageView.as_view()),
]
