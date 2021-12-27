from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import *
import os
from dotenv import load_dotenv
import requests


@api_view(['POST', 'PUT'])
def favorite(request):
    # when adding a new MyLocation record, or add a restaurant, attraction to a MyLocation record
    if request.method == 'POST':
        
        my_location_dict = {
            'traveller' : request.user.id,
        }

        location = request.data['location']
        location_id = find_location_id_or_create_new(location)
        my_location_dict['location'] = location_id

        restaurant = request.data['restaurant']
        restaurant_id = find_restaurant_id_or_create_new(restaurant)
        
        print('restaurant is: ', restaurant)

        print('my location dict is: ', my_location_dict)
        serializer = MyLocationUpdateSerializer(data=my_location_dict)
        if serializer.is_valid():
            # serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # When removing a restaurant or attraction from a MyLocation record
    elif request.method == 'PUT':
        serializer = MyLocationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    else:    
        return HttpResponseNotFound('Not found')

def find_location_id_or_create_new(location_obj):
    record = Location.objects.filter(lat=location_obj['lat'], lon = location_obj['lon'])
    if not record:
        serializer = LocationSerializer(data=location_obj)
        if serializer.is_valid():
            serializer.save()
            record = Location.objects.filter(lat=location_obj['lat'], lon = location_obj['lon'])
    
    return record[0].id

def find_restaurant_id_or_create_new(restaurant_obj):
    record = Restaurant.objects.filter(api_id=restaurant_obj['api_id'])
    if not record:
        serializer = RestaurantSerializer(data=restaurant_obj)
        if serializer.is_valid():
            serializer.save()
            record = Restaurant.objects.filter(api_id=restaurant_obj['api_id'])
    
    return record[0].id

def find_attraction_id_or_create_new(attraction_obj):
    record = Attraction.objects.filter(api_id=attraction_obj['api_id'])
    if not record:
        serializer = AttractionSerializer(data=attraction_obj)
        if serializer.is_valid():
            serializer.save()
            record = Attraction.objects.filter(api_id=attraction_obj['api_id'])
    
    return record[0].id


## The core of this functionality is the api_view decorator, which takes a list of HTTP methods that your view should respond to.
@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyLocationViewSet(ModelViewSet):

    model = MyLocation
    serializer_class = MyLocationSerializer

    def get_queryset(self):
        return MyLocation.objects.filter(traveller=self.request.user)

    def pre_save(self, obj):
        obj.traveller = self.request.user

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class AttractionViewSet(ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer