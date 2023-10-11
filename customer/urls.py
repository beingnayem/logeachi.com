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
    path('profile/', views.profileView, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('order/', views.order, name='order'),
    path('order-manage/<int:id>/', views.order_manage, name='order_manage'),
    path('track-order/', views.track_order, name='track_order'),
]