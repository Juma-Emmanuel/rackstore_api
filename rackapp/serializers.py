from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class CombinedSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')    
    full_name = serializers.CharField()
    address = serializers.CharField()
    joined_on = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'user' in data:
            data.pop('user')
        return data
    
class UserRegistrationSerializer (serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    email = serializers.CharField()
    class Meta:
        model = AppUser        
        fields = [ 'username' ,'password', 'full_name', 'address', 'email' ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = {  
            'username': validated_data['username'],         
            'email': validated_data['email'],
            'password': validated_data['password'],
        }
        user = User.objects.create_user(**user_data)        
        return AppUser.objects.create(user=user, full_name=validated_data['full_name'], address=validated_data['address'])
       

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer (serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer (serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartProductSerializer (serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'