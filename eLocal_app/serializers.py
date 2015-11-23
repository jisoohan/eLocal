from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Store, Address, Product
import base64
from django.core.files.base import ContentFile

class Base64ImageField(serializers.ImageField):
    def from_native(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super(Base64ImageField, self).from_native(data)

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
    image = Base64ImageField()

    class Meta:
        model = Store
        fields = ('id', 'user', 'address', 'image', 'name', 'has_card')

class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    image = Base64ImageField()

    class Meta:
        model = Product
        fields = ('id', 'store', 'image', 'name', 'description', 'price')

