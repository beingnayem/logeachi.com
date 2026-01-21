from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join-newsletter/', views.join_newsletter, name='join_newsletter'),
    path('search/', views.search, name='search'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('faq/', views.FAQ, name='FAQ'),
    path('about-us/', views.about_us, name='about_us'),
    path('send-query/', views.send_query, name='send_query'),
    path('new-arrivals/', views.new_arrivals, name='new_arrivals'),
    path('give-feedback/', views.give_feedback, name='give_feedback'),
]