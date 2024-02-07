from django.urls import path
from .views import get_All, get_by_Id, create_user

urlpatterns = [
    path('list/', get_All, name='user-list'),
    path('<int:user_id>/', get_by_Id, name='user-detail'),
    path('create/', create_user, name='create-user'),
]
