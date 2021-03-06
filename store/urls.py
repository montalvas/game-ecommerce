from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('update-item/', views.update_item, name='update-item'),
    path('process-order/', views.process_order, name='process-order'),
]
