from django.db import models
from django.contrib.auth.models import User
from datetime import dateti

#Cart, Product, CartItem, Order

class Product(models.Model):
    categories = [
        (1, "toys"), (2, "figurines"), (3, "books"), (4, "asian food"), (5, "posters"), (6, "notebooks"), (7, "pillows"), (8, "cosplay")
    ]
    category = models.IntegerField(choices=categories)
    name = models.CharField(max_length=150)
    price = models.FloatField()
    description = models.TextField(max_length=2000)
    count = models.IntegerField()
    photo = models.CharField()

class CartItem(models.Model):
    item_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='owner_cart')
    count = models.IntegerField()    

class Cart(models.Model):
    cart_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_cart')
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='owner_cart')

class Order(models.Models):
    user_id = models.ForeignKey(User)
    data = models.DateTimeField()
    cart = models.ForeignKey(Cart)
