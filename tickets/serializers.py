from rest_framework import serializers
from .models import SupportTicket, TicketMessage



class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = '__all__'


class SupportTicketSerializer(serializers.ModelSerializer):
    messages = TicketMessageSerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "policy",
            "subject",
            "assigned_to_role",
            "status",
            "messages",
            "created_at"
        ]
        read_only_fields = ["status", "created_at"]
