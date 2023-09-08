from django.urls import path

from networks import views

urlpatterns = [
    path(r'', views.network_list, name='list'),
    path(r'create/', views.network_create, name='create'),
    path(r'<int:network_id>/edit/', views.network_edit, name='edit'),

    path(r'asset/<int:asset_id>/create/', views.asset_network_create, name='asset_network_create'),
    path(r'asset-network/<int:asset_network_id>/edit/', views.asset_network_edit, name='asset_network_edit'),
]
