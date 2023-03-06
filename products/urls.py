from django.urls import path
from products import views

urlpatterns = [     
    path('<slug>/',  views.get_product, name='get_product'),
    path('category/<pk>', views.category_products, name='category-products'),
]