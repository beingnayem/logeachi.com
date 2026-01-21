from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('palce-order/', views.place_order, name='place_order'),
    path('success-view/', views.success_view, name='success_view'),
    path('success-view-case-on-delivery/<int:order_id>/<grand_total>/', views.success_view_case_on_delivery, name='success_view_case_on_delivery'),
]