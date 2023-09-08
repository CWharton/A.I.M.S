from django.conf.urls import include
from django.urls import path
from django.contrib import admin

from dashboard.views import dashboard
from search.views import search

urlpatterns = [

    # Admin
    path(r'admin/', admin.site.urls),

    # User Authentication
    path('', include('django.contrib.auth.urls')),

    path(r'', dashboard, name='dashboard'),
    path(r'search/', search, name='search'),

    path(r'assets/', include(("assets.urls", "assets"), namespace='assets')),
    path(r'users/', include(("users.urls", "users"), namespace='users')),
    path(r'networks/', include(("networks.urls", "networks"), namespace='networks')),
    path(r'reports/', include(("reports.urls", "reports"), namespace='reports')),
    path(r'backup/', include(("backup.urls", "backup"), namespace='backup')),
    path(r'software/', include(("software.urls", "software"), namespace='software')),
]
