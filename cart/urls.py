from django.urls import path
from . import views

urlpatterns = [
    path('add-wishlist-item/<int:id>/', views.AddWishlistItem, name='add_wishlist_item'),
    path('wishlist/', views.ShowWishlist, name='wishlist'),
    path('delete-wishlist-item/<int:id>/', views.DeleteWishlistItem, name='delete_wishlist_item'),
    path('clear-wishlist/', views.clear_wishlist, name='clear_wishlist'),
]