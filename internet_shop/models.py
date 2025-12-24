from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from datetime import datetime

#Cart, Product, CartItem, Order


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, adress, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            adress = adress,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, adress, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            adress = adress,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    adress = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = ["email", "adress"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

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
    cart_owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owner_cart')
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='owner_cart')

class Order(models.Model):
    user_id = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
