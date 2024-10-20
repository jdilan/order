from django.db import models

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True)
    customer_id = models.CharField(max_length=100)
    order_date = models.CharField(max_length=10)
    shipped_date = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    email = models.EmailField()
    
    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, to_field='order_id')
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.CharField(max_length=10)

    class Meta:
        db_table = 'order_item'
