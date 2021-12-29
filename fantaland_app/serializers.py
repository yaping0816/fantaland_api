from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from fantaland_app.models import Location
from .models import *

## Serializes current user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'id']

## Serializes new user sign ups that responds with the new user's information including a new token.

class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['token', 'username', 'password', 'id']


# Serializer models
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'categories', 'image_url', 'api_id', 'location']       

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id', 'api_id','name', 'kinds', 'location']   

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'country', 'city', 'lat', 'lon']
       

# read only, for get method to retrieve all MyLocation records, and DELETE method when deleting one record
class MyLocationSerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(many=True,read_only=True)
    attractions = AttractionSerializer(many=True,read_only=True)
    location = LocationSerializer(read_only=True)
    traveller = UserSerializer(read_only=True)
    class Meta:
        model = MyLocation
        fields = ['id', 'traveller','location', 'restaurants', 'attractions']

# used when creating new MyLocation record, or modifying restaurants and/or attractions in that record
class MyLocationUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyLocation
        fields = ['id', 'traveller','location', 'restaurants', 'attractions']




