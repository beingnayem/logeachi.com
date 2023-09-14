from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.adminPanelView, name='admin_panel_dashboard'),
    path('team-member/', views.team_memberView, name='team_member'),
    path('admin-signup-request/', views.admin_signup_requestView.as_view(), name='admin_signup_request'),
    path('admin-signup/<uidb64>/<token>/', views.admin_signupView.as_view(), name='admin_signup'),
    path('admin-request-list/', views.admin_request_listView, name='admin_request_list'),
    path('admin-request-approve/', views.admin_request_approve, name='admin_request_approve'),
    path('admin-request-decline/', views.admin_request_decline, name='admin_request_decline'),
    path('remove-admin/', views.remove_admin, name='remove_admin'),
    path('remove-user/', views.remove_user, name='remove_user'),
    path('customers/', views.customerView, name='customer_list'),
    path('products/', views.productView, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/', views.edit_product, name='edit_product'),
    path('delete-product/', views.delete_product, name='delete_product'),
    path('restock-product/', views.restock_product, name='restock_product'),
    path('individual-product-details/', views.individual_product_details, name='individual_product_details'), 
]