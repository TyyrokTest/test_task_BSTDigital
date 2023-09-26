from django.apps import AppConfig
from django.db.models.signals import post_save

class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = 'orders'

    def ready(self):
        from .signals import send_notification_to_customers
        
        post_save.connect(send_notification_to_customers, sender="robots.Robot")