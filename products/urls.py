from django.urls import path
from . import views

urlpatterns = [
    path('sub_category/<pk>/', views.sub_category_products, name='sub_category_products'),
    path('category/<pk>/', views.category_products, name='category_products'),
    path('main_category/<pk>/', views.main_category_products, name='main_category_products'),
    # path('category/<int:pk>/', views.category_products, name='category-products'),
    path('single_product_page/<int:pk>/', views.single_product_page, name='single_product_page'),
]
