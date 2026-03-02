from django.urls import path
from .views import (
    ClientCreateView, ClientListView,
    ProductCreateView, ProductListView,
    PolicyCreateView, PolicyListView,
    MemberCreateView, MemberListView,
    PolicyStatusUpdateView,
    PolicyDocumentUploadView,
    PolicyDocumentListView,
    HRPolicyListView,
    MemberPolicyView,
    MemberDeleteView,
    BulkMemberUploadView,
    EmployeeAddDependentView,
    EmployeeDeleteDependentView
)

urlpatterns = [

    # Clients
    path("clients/", ClientCreateView.as_view(), name="client-create"),
    path("clients/list/", ClientListView.as_view(), name="client-list"),

    # Products
    path("products/", ProductCreateView.as_view(), name="product-create"),
    path("products/list/", ProductListView.as_view(), name="product-list"),

    # Policies
    path("policies/", PolicyCreateView.as_view(), name="policy-create"),
    path("policies/list/", PolicyListView.as_view(), name="policy-list"),
    path("policies/<int:policy_id>/status/", PolicyStatusUpdateView.as_view(), name="policy-status-update"),
    path("policies/<int:policy_id>/documents/", PolicyDocumentListView.as_view(), name="policy-document-list"),
    path("policies/documents/upload/", PolicyDocumentUploadView.as_view(), name="policy-document-upload"),
    path("hr/policies/", HRPolicyListView.as_view(), name="hr-policy-list"),

    # Members
    path("members/", MemberCreateView.as_view(), name="member-create"),
    path("members/list/", MemberListView.as_view(), name="member-list"),
    path("members/<int:pk>/delete/", MemberDeleteView.as_view(), name="member-delete"),
    path("member/policy/", MemberPolicyView.as_view(), name="member-policy-view"),
    path("member/dependents/add/", EmployeeAddDependentView.as_view(), name="member-dependent-add"),
    path("member/dependents/<int:pk>/delete/", EmployeeDeleteDependentView.as_view(), name="member-dependent-delete"),
    path("policies/<int:policy_id>/members/bulk_upload/", BulkMemberUploadView.as_view(), name="member-bulk-upload"),
    

]