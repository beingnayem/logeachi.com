from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('palce-order/', views.place_order, name='place_order'),
    path('success-view/', views.success_view, name='success_view'),
]