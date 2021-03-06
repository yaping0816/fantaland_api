from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
import os
from django.views.decorators.csrf import csrf_exempt
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

search_radius= os.environ.get('SEARCH_RADIUS')
search_results_per_page = os.environ.get('SEARCH_RESULTS_PER_PAGE')

# 3rd party API universal requester
def api_requester(method, url, params, header_auth=None):
    if method == 'GET':
        api_response = requests.get(url, params, headers = header_auth)
        if api_response.status_code == 200:
            return HttpResponse(api_response, content_type='application/json')
        else:
            return HttpResponseBadRequest('something went wrong')
    else:
        return HttpResponseNotFound('Not found')

@csrf_exempt
def city_info(request):
    url = attraction_base_url + 'geoname'
    query = {
        'apikey': attraction_apikey,
        'name': request.GET.get('name', 'unknown')
    }
    return api_requester(request.method, url, query)

@csrf_exempt
def attractions_count(request):

    url = attraction_base_url + 'radius'
    query = {
        'apikey': attraction_apikey,
        'radius': search_radius,
        'lat':request.GET.get('lat', 'unknown'),
        'lon':request.GET.get('lon','unknown'),
        'rate':3,
        'format': 'count'
    }
    return api_requester(request.method, url, query)
 

def attractions_list(request):
    url = attraction_base_url + 'radius'
    query = {
        'apikey': attraction_apikey,
        'radius': search_radius,
        'lat':request.GET.get('lat', 'unknown'),
        'lon':request.GET.get('lon','unknown'),
        'limit':search_results_per_page,
        'rate':3,
        'offset': int(request.GET.get('page', 1)) - 1,
        'format': 'json'
    }
    return api_requester(request.method, url, query)

def attraction_detail(request,id):
    url = attraction_base_url + 'xid/' + id
    query = {
        'apikey': attraction_apikey,
    }
    return api_requester(request.method, url, query)

def restaurants_list(request):
    url = restaurant_base_url + 'search'
    query = {
        'latitude':request.GET.get('lat', 'unknown'),
        'longitude':request.GET.get('lon','unknown'),
        'radius': search_radius,
        'limit':search_results_per_page,
        'offset': int(request.GET.get('page', 1)) - 1,
        'categories':'restaurants'
    }
    return api_requester(request.method, url, query, restaurant_api_header_auth)

def restaurant_detail(request, id):
    url = restaurant_base_url + id
    return api_requester(request.method, url, None, restaurant_api_header_auth)

@csrf_exempt
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


@csrf_exempt
def process_lists(request, target):
    if target == 'restaurants':
        return restaurants_list(request)
    elif target == 'attractions':
        return attractions_list(request)
    else:
        return HttpResponseNotFound('Not Found')


@csrf_exempt
def process_detail(request, target, id):
    if target == 'restaurant':
        return restaurant_detail(request, id)
    elif target == 'attraction':
        return attraction_detail(request, id)
    else:
        return HttpResponseNotFound('Not Found')