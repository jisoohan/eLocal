from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Store, Address

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'st_number', 'st_name', 'city', 'state', 'zipcode', 'country', 'lat', 'lng')

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()

    class Meta:
        model = Store
        fields = ('id', 'user', 'address', 'name', 'has_card')

    def create(self, validated_data):
        return Store.objects.create(**validated_data)
