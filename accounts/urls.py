from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('', views.signout, name='signout'),
    path('activate/<uidb64>/<token>/',
         views.ActivateAccountView.as_view(), name='activate'),
    path('reset-pass-request/', views.RequestResetEmailView.as_view(),
         name='reset-pass-request'),
    path('reset-pass/<uidb64>/<token>/',
         views.SetNewPasswordView.as_view(), name='reset-pass'),
    path('show-profile/', views.showProfile, name='show-profile'),
    path('show-address/', views.showAddress, name='show-address'),
    path('add-address/', views.addAddress, name='add-address'),
    path('edit-address/<int:address_id>/',
         views.editAddress, name='edit-address'),
    path('delete-address/<int:address_id>/',
         views.deleteAddress, name='delete-address'),
]
