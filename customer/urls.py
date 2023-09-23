from django.urls import path
from . import views

urlpatterns = [     
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('address-book/', views.address_book, name='address_book'),
    path('add-address/', views.add_address, name='add_address'),
    path('edit-address/', views.edit_address, name='edit_address'),
    path('delete-address/', views.delete_address, name='delete_address'),
    path('make-default-shipping-address/', views.default_shipping, name='default_shipping'),
    path('make-default-billing-address/', views.deafult_billing, name='deafult_billing'),
    
]