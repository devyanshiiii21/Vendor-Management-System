from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

class VendorAPIView(APIView):
    def get(self, request):
        vendor = Vendor.objects.all()
        serializer = VendorSerializer(vendor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        
        serializer = VendorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': "New Vendor created successfully!"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VendorUpdateDeleteRetrieveAPIView(APIView):
    def get_object(self, vendor_id):
        try:
            return Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            raise NotFound('Vendor not found')
        

    def get(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    
    def put(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor, data=request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderAPIView(APIView):
    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        
        if vendor_id:
            # Filters out purchase orders by vendor ID
            orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            # If vendor ID is not provided, retrieving all purchase orders
            orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
               'data': serializer.data,
               'message' : 'Order placed successfully!'} ,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseOrderRetrieveUpdateDeleteAPIView(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            raise NotFound('Order not found')
        
    def get(self, request, po_id):
        order = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, po_id):
        order = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(order, data=request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, po_id):
        order = self.get_object(po_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


