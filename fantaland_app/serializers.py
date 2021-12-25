from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

from fantaland_app.models import Location

from .models import *


## Serializes current user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

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
        fields = ['token', 'username', 'password']


# Serializer models
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_name', 'cuisine_type', 'list', 'image']       

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id', 'attraction_name', 'list', 'image']   

class LocationSerializer(serializers.ModelSerializer):
    # restaurants = RestaurantSerializer(many=True)
    # attractions = AttractionSerializer(many=True)
    # travellers = TravellerSerializer(many=True)
    class Meta:
        model = Location
        fields = ['id', 'state', 'city', 'zipcode', 'image', 'list']
        # def to_representation(self,value):
        #     return value.state

class LocationListSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    class Meta:
        model = LocationList
        fields = ['id', 'list_name', 'traveller','locations', 'restaurants', 'attractions']




