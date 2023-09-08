from django.urls import path

from users import views

urlpatterns = [
    path(r'', views.user_list, name='user_list'),
    path(r'create/', views.user_create, name='user_create'),
    path(r'<int:user_id>/edit/', views.user_edit, name='user_edit'),
]
