from django.urls import path

from assets import views

urlpatterns = [

    path('type/', views.type_list, name='type_list'),
    path('type/create/', views.type_create, name='type_create'),
    path('type/<int:type_id>/edit/', views.type_edit, name='type_edit'),

    path('subtype/', views.subtype_list, name='subtype_list'),
    path('subtype/create/', views.subtype_create, name='subtype_create'),
    path('subtype/<int:subtype_id>/edit/', views.subtype_edit, name='subtype_edit'),

    path('status/', views.status_list, name='status_list'),
    path('status/create/', views.status_create, name='status_create'),
    path('status/<int:status_id>/edit/', views.status_edit, name='status_edit'),

    path('manufacturer/', views.manufacturer_list, name='manufacturer_list'),
    path('manufacturer/create/', views.manufacturer_create, name='manufacturer_create'),
    path('manufacturer/<int:manufacturer_id>/edit/', views.manufacturer_edit, name='manufacturer_edit'),

    path('print-queue/', views.print_queue_list, name='print-queue-list'),
    path('print-queue/<int:print_queue_id>/delete', views.print_queue_delete, name='print-queue-delete'),

    path('<int:asset_id>/edit/note/create/', views.note_create, name='note_create'),

    path('', views.asset_list, name='list'),
    path('create/', views.asset_create, name='create'),
    path('create/<list_type>/', views.asset_create_by_type, name='create_by_type'),
    path("<list_type>/", views.asset_list, name='list-type'),
    path('<int:asset_id>/edit/', views.asset_edit, name='edit'),
    path('<int:asset_id>/checkin/', views.asset_check_in, name='check-in'),
    path('<int:asset_id>/print-queue/', views.print_queue, name='print-queue'),
    path('<int:asset_id>/shelf/', views.shelf, name='shelf'),
    path('<int:asset_id>/trash/', views.asset_delete, name='trash'),
]
