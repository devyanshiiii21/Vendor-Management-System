from .views import (
    VendorAPIView, VendorUpdateDeleteRetrieveAPIView,
    PurchaseOrderAPIView, PurchaseOrderRetrieveUpdateDeleteAPIView,
    VendorHistoricalPerformanceAPIView, AcknowledgePurchaseOrderAPIView,
    VendorSignupAPIView, LoginAPIView
    ) 
from django.urls import path

urlpatterns = [

    path('signup/', VendorSignupAPIView.as_view(), name='vendor-signup'),
    path('login/', LoginAPIView.as_view(), name = 'login'),

    path('vendors/', VendorAPIView.as_view(), name='vendors'),
    path('vendors/<int:vendor_id>/', VendorUpdateDeleteRetrieveAPIView.as_view(), name='vendor-update-delete-retrieve'),

    path('purchase_orders/', PurchaseOrderAPIView.as_view(), name = 'purchase-orders'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDeleteAPIView.as_view(), name='purchase-orders-update-delete-retrieve'),

    path('api/vendors/<int:vendor_id>/historical-performance', VendorHistoricalPerformanceAPIView.as_view()),
    path('api/purchase_orders/<int:po_id>/acknowledge', AcknowledgePurchaseOrderAPIView.as_view()),
]
