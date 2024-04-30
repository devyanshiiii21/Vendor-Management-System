from .serializers import VendorSerializer
from .models import Vendor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
    



