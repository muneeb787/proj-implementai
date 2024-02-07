from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_organization, name='create-organization'),
    path('<int:organization_id>/', views.get_organization_by_id, name='organization-detail'),
    path('list/', views.get_organization_list, name='organization-list'),
]
