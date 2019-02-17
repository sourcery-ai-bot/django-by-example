from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from coupons.models import Coupon
from shop.models import Product

from ipdb import set_trace


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_subtotal_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount_cost(self):
        discount = 1
        if self.coupon.discount:
            discount = self.coupon.discount / Decimal('100')
        return sum(item.get_cost() * discount for item in self.items.all())

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - (total_cost * (self.discount / Decimal("100")))



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity

    def get_item_cost(self):
        discount = 1
        if self.order.coupon:
            discount = 1 - (self.order.coupon.discount / Decimal('100'))
        return (self.price * discount) * self.quantity
