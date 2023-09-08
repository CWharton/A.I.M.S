from django.urls import path

from backup import views

urlpatterns = [
    path(r'', views.backup_view, name='view'),
    path(r'process/', views.backup, name='backup'),
]