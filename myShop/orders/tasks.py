from celery import task
from django.core.mail import send_mail

from .models import Order


@task
def order_created(order_id):
    """
    Task to send an email notification when
    and order is successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order number {order.id}"
    message = f"""Dear {order.first_name},

You have successfully placed an order.
Your order identification number is {order.id}
    """
    # message = f"Dear {order.first_name},\n\nYou have successfully placed an order. Your order id is {order.id}"
    mail_sent = send_mail(subject, message, "admin@myshop.com", [order.email])
    return mail_sent
