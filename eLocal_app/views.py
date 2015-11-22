from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Store, Address, Product
from .serializers import UserSerializer, StoreSerializer, AddressSerializer, ProductSerializer
from .utils import json_response, check_distance
from rest_framework import permissions, viewsets, status, pagination
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes, detail_route, list_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin
from decimal import *

@permission_classes([AllowAny, ])
def base_render(request):
    return render(request, 'base.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def stores(self, request, pk=None):
        if request.method == 'GET':
            user = User.objects.get(id=pk)
            stores = Store.objects.select_related('user').filter(user_id=user.id).order_by('name')
            serializer = StoreSerializer(stores, many=True)
            return Response(serializer.data)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def create_store(self, request, pk=None):
        if request.method == 'POST':
            user = User.objects.get(id=pk)
            address_data = {
                'st_number': request.data['st_number'],
                'st_name': request.data['st_name'],
                'city': request.data['city'],
                'state': request.data['state'],
                'zipcode': request.data['zipcode'],
                'country': request.data['country'],
                'lat': request.data['lat'],
                'lng': request.data['lng']
            }
            address_serializer = AddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address = address_serializer.save()
            else:
                return Response({'error': 'Invalid address'}, status=status.HTTP_400_BAD_REQUEST)
            store = Store.objects.create(user=user, address=address, name=request.data['store_name'], has_card=request.data['has_card'])
            store_serializer = StoreSerializer(store)
            return Response(store_serializer.data)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def delete_store(self, request, pk=None):
        if request.method == 'POST':
            Store.objects.get(id=pk).delete()
            return Response({'success': 'Store deleted'})

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def stores_in_zipcode(self, request):
        lat = request.data['lat']
        lng = request.data['lng']
        stores = [];
        for store in Store.objects.all():
            if check_distance([lat, lng], [store.address.lat, store.address.lng], 10):
                store_serializer = StoreSerializer(store)
                store_data = store_serializer.data
                products = Product.objects.select_related('store').filter(store_id=store_data['id'])
                product_serializer = ProductSerializer(products, many=True)
                store_data['products'] = product_serializer.data
                stores.append(store_data)
        return Response(stores)

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def products_in_zipcode(self, request):
        lat = request.data['lat']
        lng = request.data['lng']
        products_result = []
        for store in Store.objects.all():
            if check_distance([lat, lng], [store.address.lat, store.address.lng], 10):
                store_serializer = StoreSerializer(store)
                store_data = store_serializer.data
                products = Product.objects.select_related('store').filter(store_id=store_data['id'])
                if len(products) != 0:
                    product_serializer = ProductSerializer(products, many=True)
                    for product in product_serializer.data:
                        products_result.append(product)
        return Response(products_result)

    @detail_route(methods=['get'], permission_classes=[AllowAny])
    def store_info(self, request, pk=None):
        if request.method == 'GET':
            store = Store.objects.get(id=pk)
            if not request.user.is_anonymous() and store.user.id is not request.user.id:
                return Response({'error': 'Cannot get store'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                store_serializer = StoreSerializer(store)
                return Response(store_serializer.data)

    @detail_route(methods=['post'], permission_classes=[AllowAny])
    def add_product(self, request, pk=None):
        if request.method == 'POST':
            store = Store.objects.get(id=pk)
            product = Product.objects.create(store=store, name=request.data['product_name'], description=request.data['description'], price=round(Decimal(request.data['price']), 2))
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data)

    @detail_route(methods=['post'], permission_classes=[AllowAny])
    def delete_product(self, request, pk=None):
        if request.method == 'POST':
            Product.objects.get(id=pk).delete()
            return Response({'success': 'Product Deleted'})

    @detail_route(methods=['get'], permission_classes=[AllowAny])
    def products(self, request, pk=None):
        if request.method == 'GET':
            products = Product.objects.select_related('store').filter(store_id=pk).order_by('name')
            product_serializer = ProductSerializer(products, many=True)
            return Response(product_serializer.data)

    @detail_route(methods=['post'], permission_classes=[AllowAny])
    def edit_product(self, request, pk=None):
        if request.method == 'POST':
            Product.objects.filter(id=pk).update(name=request.data['product_name'], description=request.data['description'], price=round(Decimal(request.data['price']), 2))
            product = Product.objects.get(id=pk)
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data)

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

