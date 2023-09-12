from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_sunbscriber/', views.registerSunbscriberView, name='register_sunbscriber'),
    # path('search/', views.search, name='search'),
]