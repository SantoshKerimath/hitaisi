from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    pass


class BaseAPIView(APIView):
    """
    Base API view:
    - Secure by default (JWT required)
    - Prevents drf-spectacular warnings
    - Provides default error responses
    """

    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]   # ✅ secure by default

    @extend_schema(
        responses={
            400: serializers.Serializer,
            401: serializers.Serializer,
            403: serializers.Serializer,
        }
    )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)