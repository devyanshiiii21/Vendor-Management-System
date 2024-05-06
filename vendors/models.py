from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    quality_rating_avg = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    class Meta:
        indexes = [
            models.Index(fields=['vendor_code']),
        ]

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_orders_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_orders_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=instance.delivery_date).count()
        on_time_delivery_rate = on_time_orders_count / completed_orders_count if completed_orders_count > 0 else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()
    
@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        total_completed_order = completed_orders.count()
        if total_completed_order > 0:
            sum_quality_rating=models.Sum('quality_rating')
            quality_rating_sum = completed_orders.aggregate(sum_quality_rating)['sum_quality_rating']
            quality_rating_avg = quality_rating_sum / total_completed_order
        else:
            quality_rating_avg = None
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date is not None:  
        vendor = instance.vendor
        all_po_acknowledged = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        total_po_acknowledged = all_po_acknowledged.count()
        if total_po_acknowledged > 0:
            average_response_time=Avg(models.F('acknowledgment_date') - models.F('issue_date'))
            avg_response_time = all_po_acknowledged.aggregate(average_response_time)['average_response_time']
            vendor.average_response_time = avg_response_time
            vendor.save()

@receiver(pre_save, sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, **kwargs):
    if instance.pk:  # Checks if the PurchaseOrder instance already exists
        old_instance = PurchaseOrder.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:  # Checks if status has changed
            vendor = instance.vendor
            all_po_count = PurchaseOrder.objects.filter(vendor=vendor).count()
            fulfilled_po_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
            if all_po_count > 0:
                fulfilment_rate = fulfilled_po_count / all_po_count
                vendor.fulfillment_rate = fulfilment_rate
                vendor.save()



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
