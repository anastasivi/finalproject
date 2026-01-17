from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Cart, CartItem, Order, MyUser


# Список товаров
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        
        search = request.GET.get("search_item")
        if not search is None:
            products = products.filter(name__icontains = search) 
        
        
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
        cart = Cart.objects.filter(cart_owner = request.user, is_active = True).first()
        if not cart:
            cart = Cart.objects.create(cart_owner = request.user)
        cart_item = CartItem.objects.create(item_id = product, count = count_product_kuplen, cart = cart)
        cart.save()
        cart_item.save()
        return redirect("cart_page")


# Корзина
class CartView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        cart = Cart.objects.filter(cart_owner=request.user, is_active=True).first()
        
        if cart:
            cart_items = CartItem.objects.filter(cart=cart).select_related('item_id')
            
            # Подсчет общей суммы
            total_price = 0
            total_items = 0
            
            for item in cart_items:
                item.subtotal = item.item_id.price * item.count  # Промежуточная сумма для каждого товара
                total_price += item.subtotal
                total_items += item.count
        else:
            cart_items = []
            total_price = 0
            total_items = 0
        
        context = {
            "cart_items": cart_items,
            "total_price": total_price,
            "total_items": total_items,
            "cart": cart
        }
        
        return render(request, "shop/cart_detail.html", context)
    
    def post(self, request):
        pass

# Оформление заказа
class CheckoutView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        cart = Cart.objects.filter(cart_owner = request.user, is_active = True).first()
        cart_items = CartItem.objects.filter(cart = cart)
        return render(request, "shop/checkout.html", {"cart_items": cart_items})
    
    def post(self, request):
        cart = Cart.objects.filter(cart_owner = request.user, is_active = True).first()
        if not cart:
            return redirect("cart_page")

        order = Order.objects.create(user_id=request.user, cart=cart)

        cart.is_active = False

        cart_items = CartItem.objects.filter(cart = cart)
        for item in cart_items:
            item.item_id.count-=item.count
            item.item_id.save() 

        cart.save()
        order.save()
        return redirect("order_detail_page", order_id=order.id)


# Успешное оформление заказа
class OrderSuccessView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user_id=request.user)
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
            
        is_correct_username = len(username) >= 5 and len(username) <= 30   
        is_correct_email = "@" in email

    
        user = MyUser.objects.get(id=request.user.id)
        if username and is_correct_username:
            user.username = username
        if email and is_correct_email:
            user.email = email
        if password:
            user.set_password(password) 
        if adress:
            user.adress = adress
        user.save()
        return redirect("profile_page")
    
class OrdersListView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        # Получаем все заказы пользователя
        orders = Order.objects.filter(user_id=request.user).select_related('cart').order_by('-data')
        
        # Вычисляем общую сумму для каждого заказа
        for order in orders:
            total = 0
            # Используем cartitem_set для доступа к элементам корзины
            for cart_item in order.cart.cartitem_set.all():
                total += cart_item.item_id.price * cart_item.count
            order.order_total = total
            
        return render(request, 'shop/order_list.html', {"orders": orders})