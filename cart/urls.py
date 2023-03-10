from django.urls import path
from . import views

urlpatterns = [     
    path('add-to-cart/', views.addTOcart, name='addTOcart'),
    path('show-cart/', views.Showcart, name='show-cart'),
    path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('removecart/', views.removecart, name='removecart'),
    path('add-to-wishlist/', views.addTOwishlist, name='addTOwishlist'),
    path('show-wishlist/', views.ShowWishlist, name='show-wishlist'),
    path('remove-wishlist/', views.RemoveWishlist, name='remove-wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place-order'),

]