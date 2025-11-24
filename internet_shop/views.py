from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Product, Cart, CartItem, Order


# Список товаров
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, "shop/product_list.html", {"products": products})
    
    def post(self, request):
        pass


# Детальная страница товара
class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, "shop/product_detail.html", {"product": product})
    
    def post(self, request, product_id):
        id_product_kuplen = request.POST.get("id_product_kupili")
        product = Product.objects.get(id=id_product_kuplen)
        cart_item = CartItem(item_id = product, count = 1)
        cart_item.save()
        new_cart = Cart(cart_owner=request.user, cart_item=cart_item)
        new_cart.save()

        return redirect("cart_page")


# Корзина
class CartView(View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in items)
        return render(request, "shop/cart_detail.html", {
            "cart": cart,
            "items": items,
            "total_price": total_price
        })
    
    def post(self, request):
        product_id = request.POST.get("product_id")
        if product_id:
            product = Product.objects.get(id=product_id)
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        return redirect("cart")


# Оформление заказа
class CheckoutView(View):
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
class OrderSuccessView(View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, "shop/order_success.html", {"order": order})
    
    def post(self, request, order_id):
        pass
