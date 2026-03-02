from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from .serializers import HealthCheckSerializer
from core.base_views import BaseAPIView


class HealthCheckView(BaseAPIView):

    permission_classes = [AllowAny]      # ✅ override security
    authentication_classes = []          # ✅ disable JWT completely

    @extend_schema(responses=HealthCheckSerializer)
    def get(self, request):
        return Response({
            "status": "ok",
            "service": "hitaisi"
        })