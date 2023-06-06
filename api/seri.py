from api.models import *
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class User_ser(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', "image", 'email', 'first_name', 'password')


class Product_ser(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'image', 'img_name', 'name', 'price', "description", 'star')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
class Cart_ser(serializers.ModelSerializer):
    item = Product_ser()
    user = User_ser()

    class Meta:
        model = Products
        fields = ('id',  'user', 'item')
