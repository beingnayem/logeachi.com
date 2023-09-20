from django.urls import path
from . import views

urlpatterns = [
    path('show-blog/', views.blog_show, name='show_blog'),
    path('blog-details/<int:pk>/', views.blog_details, name='blog_details'),
    path('blog-comments/<int:pk>/', views.blog_comments, name='blog_comments'),
]
