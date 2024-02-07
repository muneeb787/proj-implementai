from django.contrib import admin
from django.urls import path, include
from Users import urls as user_urls
from django.contrib.auth import urls as  authUrls
from django.contrib.auth import views as  auth_views
from Organization import urls as organization_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(user_urls)),
    path('organizations/', include(organization_urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
