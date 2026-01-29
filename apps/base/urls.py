from django.urls import path, include
from apps.base.views import CustomerDetailAPIView, CustomerListAPIView

app_name = "base"

urlpatterns = [
    path("customers/", CustomerListAPIView.as_view(), name="customer-list"),
    path("customers/<int:customer_id>/", CustomerDetailAPIView.as_view(), name="customer-detail"),
]