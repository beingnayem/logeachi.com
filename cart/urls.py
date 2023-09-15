from django.urls import path
from . import views

urlpatterns = [
    path('add-wishlist/', views.AddWishlist, name='add_wishlist'),
    path('show-wishlist/', views.ShowWishlist, name='show_wishlist'),
    path('delete-wishlist/', views.DeleteWishlist, name='delete_wishlist'),
]