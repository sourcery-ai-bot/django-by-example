from celery import task
from django.core.mail import send_mail

from .models import Order, OrderItem


@task
def order_created(order_id):
    """
    Task to send an email notification
    when an order is successfully created
    """
    order = Order.objects.get(id=order_id)
    # items = OrderItem.objects.filter(order_id=order_id)
    subject = f"Order number: {order.id}"
    message = (
        f"Dear {order.first_name},\n\n"
        "You have successfully placed an order. "
        f"Your order ID is {order.id}.\n\n"
        "Order Summary:"
    )
    # for item in items:
    #     pass
    mail_sent = send_mail(subject, message, "admin@myshop.com", [order.email])
    return mail_sent
