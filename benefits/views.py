import csv
from enum import member
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from .models import Client, Product, Policy, Member, PolicyCoverage, ProductCoverage, Policy, PolicyDocument, PremiumBuffer
from .serializers import (
    ClientSerializer,
    ProductSerializer,
    PolicySerializer,
    MemberSerializer,
    PolicyDocumentSerializer,
    PolicyStatusSerializer
)
from identity.permissions import IsRole
from benefits.services.premium_engine import calculate_member_premium


# ---- Client ----
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]


# ---- Product ----
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


# ---- Policy ----
class PolicyCreateView(generics.CreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        policy = serializer.save()

        # Freeze coverages from product into policy_coverages
        product_coverages = ProductCoverage.objects.filter(product=policy.product)

        for cov in product_coverages:
            PolicyCoverage.objects.create(
                policy=policy,
                coverage_name=cov.coverage_name,
                is_covered=cov.is_covered,
                sublimit_amount=cov.sublimit_amount if cov.has_sublimit else None
            )
        
        policy = serializer.save()

        PremiumBuffer.objects.create(policy=policy)



class PolicyListView(generics.ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [permissions.AllowAny]


# ---- Members ----
class MemberCreateView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.AllowAny]


class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.AllowAny]


class PolicyStatusUpdateView(APIView):
    permission_classes = [IsRole]
    allowed_roles = ['ops_user', 'org_admin']  # ops issues, HR accepts

    def patch(self, request, policy_id):
        policy = Policy.objects.get(id=policy_id)
        new_status = request.data.get("status")

        # Enforce transition rules
        if new_status == "issued" and request.user.role != "ops_user":
            return Response({"error": "Only Ops can issue policy"}, status=403)

        if new_status == "in_force" and request.user.role != "org_admin":
            return Response({"error": "Only HR Admin can activate policy"}, status=403)

        policy.status = new_status
        policy.save()
        return Response({"status": "updated", "new_status": policy.status})



@extend_schema(request=PolicyDocumentSerializer)
class PolicyDocumentUploadView(generics.CreateAPIView):
    queryset = PolicyDocument.objects.all()
    serializer_class = PolicyDocumentSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]


class PolicyDocumentListView(generics.ListAPIView):
    serializer_class = PolicyDocumentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        policy_id = self.kwargs['policy_id']
        return PolicyDocument.objects.filter(policy_id=policy_id)


@extend_schema(request=PolicyStatusSerializer, responses=PolicyStatusSerializer)
class PolicyStatusUpdateView(APIView):
    permission_classes = [IsRole]
    allowed_roles = ['ops_user', 'org_admin']

    def patch(self, request, policy_id):
        policy = Policy.objects.get(id=policy_id)
        new_status = request.data.get("status")

        if new_status == "issued" and request.user.role != "ops_user":
            return Response({"error": "Only Ops can issue policy"}, status=403)

        if new_status == "in_force" and request.user.role != "org_admin":
            return Response({"error": "Only HR Admin can activate policy"}, status=403)

        policy.status = new_status
        policy.save()
        return Response({"status": policy.status})


class HRPolicyListView(generics.ListAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsRole]
    allowed_roles = ['org_admin']

    def get_queryset(self):
        # HR belongs to organization
        org = self.request.user.organization
        return Policy.objects.filter(client__organization=org)


class MemberPolicyView(generics.RetrieveAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsRole]
    allowed_roles = ['member_user']

    def get_object(self):
        member = Member.objects.get(user=self.request.user)
        return member.policy



class MemberDeleteView(generics.DestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsRole]
    allowed_roles = ['org_admin']

    def perform_destroy(self, instance):
        buffer, created = PremiumBuffer.objects.get_or_create(policy=instance.policy)

        buffer.premium_used -= instance.premium

        buffer.recalc()
        instance.delete()


@extend_schema(request=None, responses=None, description="Bulk upload members CSV")
class BulkMemberUploadView(APIView):
    permission_classes = [IsRole]
    allowed_roles = ['org_admin']
    parser_classes = [MultiPartParser]

    def post(self, request, policy_id):
        file = request.FILES['file']
        policy = Policy.objects.get(id=policy_id)

        decoded = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)

        for row in reader:
            data = {
                "policy": policy.id,
                "name": row['name'],
                "relation": row['relation'],
                "employee_code": row['employee_code'],
                "date_of_birth": row['dob'],
                "gender": row['gender'],
                "age": int(row['age']),
                "sum_insured": int(row['sum_insured']),
                "cover_start_date": row.get('start_date') or None,
                "cover_end_date": row.get('end_date') or None,
            }

            serializer = MemberSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({"status": "bulk upload complete"})


class EmployeeAddDependentView(generics.CreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsRole]
    allowed_roles = ['member_user']

    def perform_create(self, serializer):
        # Logged-in employee
        user = self.request.user

        # Find employee member record
        employee_member = Member.objects.get(user=user)

        # Force same policy and employee_code
        serializer.save(
            policy=employee_member.policy,
            employee_code=employee_member.employee_code
        )



@extend_schema(responses=MemberSerializer)
class EmployeeDeleteDependentView(generics.DestroyAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsRole]
    allowed_roles = ['member_user']
    queryset = Member.objects.all()

    def perform_destroy(self, instance):
        user = self.request.user
        employee_member = Member.objects.get(user=user)

        if instance.employee_code != employee_member.employee_code:
            raise PermissionDenied("Cannot delete members outside your family")

        buffer, _ = PremiumBuffer.objects.get_or_create(policy=instance.policy)
        buffer.premium_used -= instance.premium
        buffer.recalc()
        instance.delete()
