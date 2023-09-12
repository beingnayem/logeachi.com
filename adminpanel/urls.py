from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.adminPanelView, name='admin_panel_dashboard'),
    path('team-member/', views.team_memberView, name='team_member'),
    path('admin-request/', views.admin_request, name='admin_request'),
    path('admin-request-list/', views.admin_request_listView, name='admin_request_list'),
    path('admin-request-approve/', views.admin_request_approve, name='admin_request_approve'),
    path('admin-request-decline/', views.admin_request_decline, name='admin_request_decline'),
    path('remove-admin/', views.remove_admin, name='remove_admin'),
    path('remove-user/', views.remove_user, name='remove_user'),

]