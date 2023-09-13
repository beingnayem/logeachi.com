from django.urls import path
from . import views

urlpatterns = [
    path('add-wishlist/', views.AddWishlist, name='add_wishlist'),
]