

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('request-pickup/', views.request_pickup, name='request_pickup'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-update-issue/<int:issue_id>/', views.admin_update_issue, name='admin_update_issue'),
    path('admin-update-pickup/<int:pickup_id>/', views.admin_update_pickup, name='admin_update_pickup'),
    path('logout/', views.logout_view, name='logout'),
    path('add-image/', views.add_image, name='add_image'),
]
