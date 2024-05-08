from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, attr):
        if attr['password'] != attr['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attr

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        vendor = Vendor.objects.create(**validated_data)
        vendor.set_password(validated_data['password'])
        vendor.save()
        return vendor
    


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

