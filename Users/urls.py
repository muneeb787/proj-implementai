from django.urls import path
from .views import get_All, get_by_Id, create_user,get_csrf_token,login

urlpatterns = [
    path('list/', get_All, name='user-list'),
    path('<int:user_id>/', get_by_Id, name='user-detail'),
    path('create/', create_user, name='create-user'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('login/', login, name='user-login'),
]
