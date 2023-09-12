from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.adminPanelView, name='admin_panel_dashboard'),
    path('team-member/', views.team_memberView, name='team_member'),
    path('admin-request/', views.admin_request, name='admin_request'),
    path('admin-request-list/', views.admin_requestsView, name='admin_request_list'),
    path('admin-request-approve/', views.admin_request_approveView, name='admin_request_approve'),
    path('admin-request-decline/<int:id>/', views.admin_request_declineView, name='admin_request_decline'),
    path('remove-admin/', views.remove_adminView, name='remove_admin'),
    path('remove-user/', views.remove_userView, name='remove_user'),

]