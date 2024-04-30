from .views import VendorAPIView
from django.urls import path

urlpatterns = [
    path('vendors/', VendorAPIView.as_view(), name='vendors'),
]