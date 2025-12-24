from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Cart, CartItem, Order


# Список товаров
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        
        search = request.GET.get("search_item")
        if not search is None:
            products = products.filter(name__contains = search) 
        
        
        return render(request, "shop/product_list.html", {"products": products})

    
    def post(self, request):
        pass


# Детальная страница товара
class ProductDetailView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, "shop/product_detail.html", {"product": product})
    
    def post(self, request, product_id):
        id_product_kuplen = request.POST.get("id_product_kupili")
        count_product_kuplen = int(request.POST.get("count_product_kupili"))
        product = Product.objects.get(id=id_product_kuplen)
        cart_item = CartItem(item_id = product, count = count_product_kuplen)
        cart_item.save()
        new_cart = Cart(cart_owner=request.user, cart_item=cart_item)
        new_cart.save()

        return redirect("cart_page")


# Корзина
class CartView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        cart = Cart.objects.filter(cart_owner=request.user)
        cart_items = [item.cart_item for item in cart]
        return render(request, "shop/cart_detail.html", {"cart_items": cart_items})
    
    def post(self, request):
        pass


# Оформление заказа
class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        items = CartItem.objects.filter(cart=cart)
        return render(request, "shop/checkout.html", {"cart": cart, "items": items})
    
    def post(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        order = Order.objects.create(user=request.user, total=cart.get_total())
        for item in cart.items.all():
            order.items.add(item)
        cart.is_active = False
        cart.save()
        return redirect("order_success", order_id=order.id)


# Успешное оформление заказа
class OrderSuccessView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, "shop/order_success.html", {"order": order})
    
    def post(self, request, order_id):
        pass

class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        return render(request, "shop/profile.html")
    
    def post(self, request):
        pass

class ProfileEditView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        return render(request, "shop/profile_edit.html")
    
    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        adress = request.POST.get("adress")
