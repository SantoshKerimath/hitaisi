from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import SupportTicket
from .serializers import SupportTicketSerializer, TicketMessageSerializer
from identity.permissions import IsRole

class CreateTicketView(generics.CreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsRole]
    allowed_roles = ['org_admin', 'ops_user', 'broker_user']

    def perform_create(self, serializer):
        serializer.save(raised_by=self.request.user)


class AssignedTicketsView(generics.ListAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsRole]
    allowed_roles = ['org_admin', 'ops_user', 'broker_user']

    def get_queryset(self):
        return SupportTicket.objects.filter(
            assigned_to_role=self.request.user.role
        ).order_by('-created_at')



class AddTicketMessageView(generics.CreateAPIView):
    serializer_class = TicketMessageSerializer
    permission_classes = [IsRole]
    allowed_roles = ['org_admin', 'ops_user', 'broker_user']

    def perform_create(self, serializer):
        msg = serializer.save(sender=self.request.user)

        # Optional: if status provided in request, update ticket
        new_status = self.request.data.get("status")
        if new_status:
            msg.ticket.status = new_status
            msg.ticket.save()


class UpdateTicketStatusView(generics.UpdateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [IsRole]
    allowed_roles = ['org_admin', 'ops_user', 'broker_user']

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        new_status = request.data.get("status")

        # Valid transitions
        if ticket.status == "open" and new_status == "in_progress":
            ticket.status = "in_progress"
        elif ticket.status == "in_progress" and new_status == "closed":
            ticket.status = "closed"
        else:
            return Response(
                {"error": "Invalid status transition"},
                status=400
            )

        ticket.save()
        return Response({"status": ticket.status})
