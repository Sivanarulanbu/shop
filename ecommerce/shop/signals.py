from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .models import Order, OrderItem, OrderStatus, Product

@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    """
    Update product stock when an order item is created or updated
    """
    if created:  # Only reduce stock when the order item is first created
        product = instance.product
        product.stock -= instance.quantity
        product.save()

@receiver(post_delete, sender=OrderItem)
def restore_product_stock(sender, instance, **kwargs):
    """
    Restore product stock when an order item is deleted
    """
    product = instance.product
    product.stock += instance.quantity
    product.save()

@receiver(pre_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    """
    Check if product stock is low and send notification
    """
    try:
        old_instance = Product.objects.get(pk=instance.pk)
        # Check if stock has been updated
        if old_instance.stock != instance.stock and instance.stock <= 5:
            # Send low stock notification
            subject = f'Low Stock Alert: {instance.name}'
            message = f'Product {instance.name} has low stock ({instance.stock} remaining)'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True,
            )
    except Product.DoesNotExist:
        pass  # New product being created

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    """
    Send notifications when order status changes
    """
    if not created and instance.status != instance.tracker.previous('status'):
        # Order status has changed
        context = {
            'order': instance,
            'status': instance.get_status_display(),
            'tracking_number': instance.tracking_number
        }
        
        # Send email notification
        html_message = render_to_string('shop/email/order_status_update.html', context)
        plain_message = render_to_string('shop/email/order_status_update.txt', context)
        
        send_mail(
            f'Order #{instance.id} Status Update',
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            html_message=html_message,
            fail_silently=True,
        )

@receiver(post_save, sender=OrderStatus)
def create_order_status_history(sender, instance, created, **kwargs):
    """
    Update order status when a new status update is created
    """
    if created:
        order = instance.order
        order.status = instance.status
        if instance.status == 'delivered':
            order.delivered_date = timezone.now()
        elif instance.status == 'shipped':
            order.shipped_date = timezone.now()
        order.save()

@receiver(pre_save, sender=Product)
def handle_product_availability(sender, instance, **kwargs):
    """
    Automatically update product availability based on stock
    """
    if instance.stock <= 0:
        instance.available = False
    elif instance.stock > 0 and not instance.available:
        # Only set to True if it was previously False and now has stock
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            if old_instance.stock <= 0:
                instance.available = True
        except Product.DoesNotExist:
            # New product being created with stock
            instance.available = True