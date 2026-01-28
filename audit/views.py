from django.shortcuts import render
from .models import AuditEvent
from .serializers import AuditEventSerializer
from rest_framework import generics
from identity.permissions import IsRole

class AuditEventListView(generics.ListAPIView):
    serializer_class = AuditEventSerializer
    permission_classes = [IsRole]
    allowed_roles = ['platform_admin', 'ops_user']

    def get_queryset(self):
        qs = AuditEvent.objects.all().order_by('-timestamp')

        user_id = self.request.query_params.get('user')
        if user_id:
            qs = qs.filter(user_id=user_id)

        return qs
