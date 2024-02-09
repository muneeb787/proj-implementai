from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_lead, name='create_lead'),
    path('<int:lead_id>/', views.get_lead_by_id, name='get_lead'),
    path('getAll', views.get_leads_list, name='get_lead'),
    path('initiate-call/<int:lead_id>', views.initiate_phone_call, name='vapi_call_initiate'),
]
