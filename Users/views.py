from django.contrib.auth.models import User
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_All(request):
    users = User.objects.all()
    user_data = [{'id': user.id, 'username': user.username , 'email': user.email} for user in users]
    return Response(user_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_by_Id(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_data = {'id': user.id, 'username': user.username}
        return Response(user_data)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({"error": "Please provide username, password, and email"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
