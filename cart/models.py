from django.db import models
from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'كاش عند الاستلام'),
        ('visa', 'فيزا'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.price * self.quantity