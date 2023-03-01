from django.urls import path
from . import views

urlpatterns = [     
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('', views.signout, name='signout'),
    # path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
]