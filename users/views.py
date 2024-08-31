from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt
import bcrypt
from django.conf import settings
from datetime import datetime, timedelta


@api_view(['POST'])
def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print('hashed password', hashed_password)
    user = User(username=username, password=hashed_password.decode('utf-8'))
    user.save()
    return Response({'message': 'User created successfully'})


@api_view(['POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=400)

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)
