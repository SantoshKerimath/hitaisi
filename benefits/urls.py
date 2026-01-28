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
    path('clients/', ClientCreateView.as_view()),
    path('clients/list/', ClientListView.as_view()),

    # Products
    path('products/', ProductCreateView.as_view()),
    path('products/list/', ProductListView.as_view()),

    # Policies
    path('policies/', PolicyCreateView.as_view()),
    path('policies/list/', PolicyListView.as_view()),

    # Members
    path('members/', MemberCreateView.as_view()),
    path('members/list/', MemberListView.as_view()),
    path('policies/<int:policy_id>/status/', PolicyStatusUpdateView.as_view()),

    path('policies/<int:policy_id>/documents/', PolicyDocumentListView.as_view()),
    path('policies/documents/upload/', PolicyDocumentUploadView.as_view()),

    path('hr/policies/', HRPolicyListView.as_view()),
    path('member/policy/', MemberPolicyView.as_view()),
    path('members/<int:pk>/delete/', MemberDeleteView.as_view()),
    path('policies/<int:policy_id>/members/bulk_upload/', BulkMemberUploadView.as_view()),

    path('member/dependents/add/', EmployeeAddDependentView.as_view()),
    path('member/dependents/<int:pk>/delete/', EmployeeDeleteDependentView.as_view()),


    

]