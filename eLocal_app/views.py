from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Store, Address
from .serializers import UserSerializer, StoreSerializer, AddressSerializer
from .utils import json_response
from rest_framework import permissions, viewsets, status, pagination
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin

@permission_classes([AllowAny, ])
def base_render(request):
    return render(request, 'base.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer

    @detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def stores(self, request, pk=None):
        if request.method == 'GET':
            user = User.objects.get(id=pk)
            stores = Store.objects.select_related('user').filter(user_id=user.id)
            serializer = StoreSerializer(stores, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            user = User.objects.get(id=pk)
            address_data = {
                'st_number': request.data['st_number'],
                'st_name': request.data['st_name'],
                'city': request.data['city'],
                'state': request.data['state'],
                'zipcode': request.data['zipcode'],
                'country': request.data['country'],
                'lat': 0,
                'lng': 0
            }
            address_serializer = AddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address = address_serializer.save()
            else:
                return Response({'error': 'Invalid address'}, status=status.HTTP_400_BAD_REQUEST)
            store_data = {
                'name': request.data['store_name'],
                'user': user,
                'address': address,
                'has_card': request.data['has_card']
            }
            store_serializer = StoreSerializer(data=store_data)
            if store_serializer.is_valid():
                store = store_serializer.save()
            else:
                return Response({'error': 'Invalid store'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(store_serializer.data)

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        if User.objects.filter(username__iexact=username).exists():
            return json_response({'error': 'Username already exists'}, status=400)
        else:
            user = User.objects.create_user(username, email=None, password=password)
            auth_serializer = AuthTokenSerializer(data={'username': username, 'password': password})
            if auth_serializer.is_valid():
                token, created = Token.objects.get_or_create(user=user)
                print(token.key)
                print(user.username)
                print(user.id)
                return json_response({'token': token.key, 'username': user.username, 'userId': user.id})
            else:
                return json_response({'error': 'Register failed'}, status=400)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({'error': 'Invalid Call'}, status=405)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    if request.method == 'POST':
        auth_serializer = AuthTokenSerializer(data=request.data)
        if auth_serializer.is_valid():
            user = auth_serializer.validated_data['user']
            user_serializer = UserSerializer(user)
            token, created = Token.objects.get_or_create(user=user)
            return json_response({'token': token.key,
                                 'username': user_serializer.data['username'],
                                 'userId': user_serializer.data['id']})
        else:
            return json_response({'error': 'Invalid Username/Password'}, status=400)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({'error': 'Invalid Call'}, status=405)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def logout(request):
    if request.method == 'POST':
        return json_response({'status': 'success'})
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({'error': 'Invalid Call'}, status=405)

