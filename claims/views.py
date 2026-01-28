from rest_framework import generics
from .models import Claim
from .serializers import ClaimSerializer
from identity.permissions import IsRole

class ClaimCreateView(generics.CreateAPIView):
    serializer_class = ClaimSerializer
    permission_classes = [IsRole]
    allowed_roles = ['member_user', 'ops_user']


class ClaimListView(generics.ListAPIView):
    serializer_class = ClaimSerializer
    permission_classes = [IsRole]
    allowed_roles = ['ops_user']

    queryset = Claim.objects.all().order_by('-created_at')
