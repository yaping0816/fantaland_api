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

load_dotenv()  # take environment variables from .env
attraction_base_url = 'https://api.opentripmap.com/0.1/en/places/'
attraction_apikey = os.environ.get('OPEN_TRIP_MAP_API_KEY')

restaurant_base_url='https://api.yelp.com/v3/businesses/'
restaurant_api_header_auth = {
   "Authorization": "Bearer " + os.environ.get('YELP_API_KEY')
}

weather_base_url = 'https://api.openweathermap.org/data/2.5/onecall'
weather_api_key = os.environ.get('OPEN_WEATHER_API_KEY')

# 3rd party API universal requester
def api_requester(method, url, params, header_auth=None):
    if method == 'GET':
        api_response = requests.get(url, params, headers = header_auth)
        if api_response.status_code == 200:
            return HttpResponse(api_response, content_type='application/json')
        
        return HttpResponseBadRequest('something went wrong')
    else:
        return HttpResponseNotFound('Not found')

def city_info(request):
    url = attraction_base_url + 'geoname'
    query = {
        'apikey': attraction_apikey,
        'name': request.GET.get('name', 'unknown')
    }
    return api_requester(request.method, url, query)

def attractions_count_by_city(request):

    url = attraction_base_url + 'radius'
    query = {
        'apikey': attraction_apikey,
        'radius': 1600,
        'lat':request.GET.get('lat', 'unknown'),
        'lon':request.GET.get('lon','unknown'),
        'rate':3,
        'format': 'count'
    }
    return api_requester(request.method, url, query)
 
def attractions_list_by_city(request):
    url = attraction_base_url + 'radius'
    query = {
        'apikey': attraction_apikey,
        'radius': 1600,
        'lat':request.GET.get('lat', 'unknown'),
        'lon':request.GET.get('lon','unknown'),
        'limit':10,
        'rate':3,
        'offset': int(request.GET.get('page', 1)) - 1,
        'format': 'json'
    }
    return api_requester(request.method, url, query)

def attraction_detail(request,xid):
    url = attraction_base_url + 'xid/' + xid
    query = {
        'apikey': attraction_apikey,
    }
    return api_requester(request.method, url, query)

def restaurants_list(request):
    url = restaurant_base_url + 'search'
    query = {
        'latitude':request.GET.get('lat', 'unknown'),
        'longitude':request.GET.get('lon','unknown'),
        'radius': 1600,
        'limit':10,
        'offset': int(request.GET.get('page', 1)) - 1,
        'categories':'restaurants'
    }
    return api_requester(request.method, url, query, restaurant_api_header_auth)

def restaurant_detail(request, id):
    url = restaurant_base_url + id
    return api_requester(request.method, url, None, restaurant_api_header_auth)

def weather_info(request):
    url = weather_base_url
    query = {
        'appid' : weather_api_key,
        'lat':request.GET.get('lat', 'unknown'),
        'lon':request.GET.get('lon','unknown'),
        'units': 'imperial',
        'exclude':'minutely,hourly'
    }
    return api_requester(request.method, url, query)


def add_to_favorite(requests):
    return HttpResponseNotFound('Not found')


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