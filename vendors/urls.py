from .views import (
    VendorAPIView, VendorUpdateDeleteRetrieveAPIView,
    PurchaseOrderAPIView, PurchaseOrderRetrieveUpdateDeleteAPIView
    ) 
from django.urls import path

urlpatterns = [
    path('vendors/', VendorAPIView.as_view(), name='vendors'),
    path('vendors/<int:vendor_id>/', VendorUpdateDeleteRetrieveAPIView.as_view(), name='vendor-update-delete-retrieve'),

    path('purchase_orders/', PurchaseOrderAPIView.as_view(), name = 'purchase-orders'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDeleteAPIView.as_view(), name='purchase-orders-update-delete-retrieve'),
]