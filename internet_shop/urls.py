from django.contrib import admin
from django.urls import path

from internet_shop.views import *

urlpatterns = [
    path('', ProductListView.as_view(), name="home_page"),
    path('product/<int:product_id>', ProductDetailView.as_view(), name="product_detail_page"),
    path('cart/', CartView.as_view(), name="cart_page"),
    path('order/', CheckoutView.as_view(), name="order_page"),
    path('order/success/', OrderSuccessView.as_view(), name="order_detail_page"),   
    path('profile/', ProfileView.as_view(), name="profile_page"),   
    path('profile/edit', ProfileEditView.as_view(), name="edit_page")
]
    