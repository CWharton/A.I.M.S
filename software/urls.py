from django.urls import path

from software import views

urlpatterns = [
    path(r'', views.software_list, name='list'),
    path(r'create/', views.software_create, name='create'),
    path(r'<int:software_id>/edit/', views.software_edit, name='edit'),

    path(r'asset/<int:asset_id>/license/create/', views.asset_license_create, name='asset_license_create'),
    path(r'asset/<int:asset_id>/license/delete/<int:license_id>', views.asset_license_delete, name='asset_license_delete'),
]
