from django.urls import path

from reports import views

urlpatterns = [
    # url(r'^$', views.network_list, name='list'),
    path(r'audit/', views.audit_report, name='audit_report'),
    path(r'subnet_ip_report/', views.subnet_ip_select, name='subnet_ip_report'),
    path(r'subnet_ip_report/<int:network_id>/', views.subnet_ip_report, name='subnet_ip_report'),
    path(r'inventory/', views.inventory_report, name='inventory_report'),
]


