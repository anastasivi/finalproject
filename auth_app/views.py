from django.shortcuts import render, redirect
from django.contrib.auth import (
    login as auth_login, 
    authenticate as auth_authenticate,
    logout as auth_logout
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import View

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_page')
        form = UserCreationForm()
        return render(request, 'auth_app/register.html', {"form": form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('task_list')
        return render(request, 'auth_app/register.html', {"form": form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_page')
        form = AuthenticationForm()
        return render(request, 'auth_app/login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth_authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home_page')
        return render(request, 'auth_app/login.html', {"form": form})
    
class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('login')