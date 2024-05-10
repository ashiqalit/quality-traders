from django.core.management.base import BaseCommand
from store.models import Order
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    help = "Update created_at field of orders to timezone aware"

    def handle(self, *args, **kwargs):
        orders = Order.objects.all()
        user_timezone = pytz.timezone('Asia/Kolkata')
        for order in orders:
             if not order.created_at.tzinfo:
                aware_timezone = user_timezone.localize(order.created_at)
                order.created_at = aware_timezone
                order.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated created_at field timezone for orders'))