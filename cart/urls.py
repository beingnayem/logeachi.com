from django.urls import path
from . import views

urlpatterns = [
    # Wishlist
    path('add-wishlist-item/<int:id>/', views.AddWishlistItem, name='add_wishlist_item'),
    path('wishlist/', views.ShowWishlist, name='wishlist'),
    path('delete-wishlist-item/<int:id>/', views.DeleteWishlistItem, name='delete_wishlist_item'),
    path('clear-wishlist/', views.clear_wishlist, name='clear_wishlist'),
    
    # Cart
    path('add-to-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('show-cart', views.show_cart, name='show_cart'),
    path('delete-cart/<int:id>', views.delete_cart, name='delete_cart'),
    path('clear-cart', views.clear_cart, name='clear_cart'),
]