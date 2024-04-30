from .views import VendorAPIView, VendorUpdateDeleteRetrieveAPIView
from django.urls import path

urlpatterns = [
    path('vendors/', VendorAPIView.as_view(), name='vendors'),
    path('vendors/<int:vendor_id>/', VendorUpdateDeleteRetrieveAPIView.as_view(), name='vendor-update-delete-retrieve'),
]