#-*- coding: utf-8 -*-
from django.db.models.signals import post_save
from robots.models import Robot
from orders.models import Order
from django.dispatch import receiver
from django.core.mail import EmailMessage

def custom_send_mail(to, model, version):
    """Sending email to customer"""
    subj = f"Робот {model}-{version} теперь в наличии!"
    body = ("Добрый день!\n"
            f"Недавно вы интересовались нашим роботом модели {model}, версии {version}.\n"
            "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.\n"      
            "С уважением Компания" 
            )
    from_email = "admin@company.com"
    
    email = EmailMessage(
        subject=subj,
        body=body,
        from_email=from_email,
        to=[to],
    )
    email.send()

@receiver(post_save, sender=Robot, weak=False)
def send_notification_to_customers(sender, instance, *args, **kwargs):
    """Function that checks saved Robot instance whether there are customers waiting for this robot"""
    qs = (
            Order.objects.filter(robot_serial=instance.serial)
                         .values('customer', 'customer__email', 'robot_serial')
                         .distinct()
    )
    
    if len(qs) > 0:
        for order in qs:
            custom_send_mail(to=order['customer__email'],
                             model=order['robot_serial'].split('-')[0],
                             version=order['robot_serial'].split('-')[1])