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



## The core of this functionality is the api_view decorator, which takes a list of HTTP methods that your view should respond to.
@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


def city_info(req):
    if req.method == 'GET':
        url = attraction_base_url + 'geoname'
        city_name = req.GET.get('name', 'unknown')
        query = {
            'apikey': attraction_apikey,
            'name': city_name
        }
        api_response = requests.get(url, params = query)
        if api_response.status_code == 200:
            return HttpResponse(api_response, content_type='application/json')
        
        return HttpResponseBadRequest('something went wrong')
    else:
        return HttpResponseNotFound('Not found')

def attractions_count_by_city(request):
    if request.method == 'GET':
        url = attraction_base_url + 'radius'
        Latitude = request.GET.get('lat', 'unknown')
        Longitude = request.GET.get('lon','unknown')
        query = {
            'apikey': attraction_apikey,
            'radius': 1600,
            'lat':Latitude,
            'lon':Longitude,
            'rate':3,
            'format': 'count'
        }
        api_response = requests.get(url, params = query)
        if api_response.status_code == 200:
            return HttpResponse(api_response, content_type='application/json')
        
        return HttpResponseBadRequest('something went wrong')
    else:
        return HttpResponseNotFound('Not found')

def attractions_list_by_city(request):
    if request.method == 'GET':
        url = attraction_base_url + 'radius'
        Latitude = request.GET.get('lat', 0)
        Longitude = request.GET.get('lon',0)
        page = request.GET.get('page', 1)
        query = {
            'apikey': attraction_apikey,
            'radius': 1600,
            'lat':Latitude,
            'lon':Longitude,
            'limit':10,
            'rate':3,
            'offset': int(page) - 1,
            'format': 'json'
        }
        api_response = requests.get(url, params = query)
        if api_response.status_code == 200:
            return HttpResponse(api_response, content_type='application/json')
        
        return HttpResponseBadRequest('something went wrong')
    else:
        return HttpResponseNotFound('Not found')

def attraction_detail(request,xid):
    if request.method == 'GET':
        url = attraction_base_url + 'xid/' + xid
        query = {
            'apikey': attraction_apikey,
        }
        api_response = requests.get(url, params = query)
        if api_response.status_code == 200:
            return HttpResponse(api_response, content_type='application/json')
        
        return HttpResponseBadRequest('something went wrong')
    else:
        return HttpResponseNotFound('Not found')


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


class LocationListViewSet(ModelViewSet):
    queryset = LocationList.objects.all()
    serializer_class = LocationListSerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class AttractionViewSet(ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer