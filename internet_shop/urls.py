from django.contrib import admin
from django.urls import path

from main.views import *

urlpatterns = [
    path('', BaseView.as_view(), name='cbv_page'),
    path('test_page/', BaseView.as_view(), name='cbv_page2')
]
    