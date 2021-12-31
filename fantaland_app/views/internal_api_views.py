from django.core.checks.messages import Error
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from rest_framework.viewsets import ModelViewSet
from ..models import *

@api_view(['POST'])
def favorite(request):
    # adding a new MyLocation record
    if request.method != 'POST':
        return HttpResponseNotFound('Not found')
        
    my_location_dict = {
        'traveller' : request.user.id,
    }

    location_data = request.data
    try:
        location_id = find_location_id_or_create_new(location_data)
    except:
        return HttpResponseBadRequest('Invalid input data')
    my_location_dict['location'] = location_id

    serializer = MyLocationUpdateSerializer(data=my_location_dict)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif serializer.errors['non_field_errors']:
        # if the user - location set already exist, find and return it.
        return Response(find_my_location_record(request.user.id, location_id),status=status.HTTP_200_OK )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
def find_my_location_record(user_id, location_id):
    try:
        record = MyLocation.objects.get(traveller=user_id, location=location_id)
        return MyLocationUpdateSerializer(record).data
    except MyLocation.DoesNotExist:
        return 0

def find_location_id_or_create_new(location_obj):
    try:
        record = Location.objects.get(lat=location_obj['lat'], lon = location_obj['lon'])
    except Location.DoesNotExist:
        serializer = LocationSerializer(data=location_obj)
        if serializer.is_valid(raise_exception=True):
            record = serializer.save()
    
    return record.id

def find_restaurant_id_or_create_new(restaurant_obj):
    try:
        record = Restaurant.objects.get(api_id=restaurant_obj['api_id'])
    except Restaurant.DoesNotExist:
        serializer = RestaurantSerializer(data=restaurant_obj)
        if serializer.is_valid(raise_exception=True):
            record = serializer.save()
    
    return record.id

def find_attraction_id_or_create_new(attraction_obj):
    try:
        record = Attraction.objects.get(api_id=attraction_obj['api_id'])
    except Attraction.DoesNotExist:
        serializer = AttractionSerializer(data=attraction_obj)
        if serializer.is_valid(raise_exception=True):
            record = serializer.save()
    
    return record.id

@api_view(['POST'])
def add_restaurant_or_attraction_to_favorite(request, my_location_id, target):
    if target != 'restaurants' and target != 'attractions':
        return HttpResponseNotFound('Not found')

    if request.method != "POST":
        return HttpResponseNotFound('Not found')

    # step 1, the MyLocation record MUST exist
    try:
        my_location_record = MyLocation.objects.get(pk=my_location_id)
    except MyLocation.DoesNotExist:
        return HttpResponse(status=404)
    # step 2, use serializer to parse model data into dict 
    my_location_data = MyLocationUpdateSerializer(my_location_record).data

    # step 3, get the restaurant or attraction id, or create new and get id
    target_data = request.data
    try:
        target_id = find_restaurant_id_or_create_new(target_data) if target == 'restaurants' else find_attraction_id_or_create_new(target_data)
    except Exception:
        print(Exception)
        # return HttpResponseBadRequest('Invalid input data1')

    # step 4, add the restaurant or attraction id to list
    try:
        my_location_data[target].append(target_id)
    except:
        return HttpResponseBadRequest('Invalid input data2')
    # step 5, save updated record
    serializer = MyLocationUpdateSerializer(my_location_record, data=my_location_data)
    if serializer.is_valid():
        serializer.save()
    
    return HttpResponse(status=201)

@api_view(['DELETE'])
@csrf_exempt
def remove_restaurant_or_attraction_from_favorite(request, my_location_id, target,target_id):
    # path only support restaurants or attractions
    # this function logic is different than adding restaurants or attractions to MyLocation record
    if target != 'restaurants' and target != 'attractions':
        return HttpResponseNotFound('Not found')

    if request.method != "DELETE":
        return HttpResponseNotFound('Not found')

    # step 1, the MyLocation record MUST exist
    try:
        my_location_record = MyLocation.objects.get(pk=my_location_id)
    except MyLocation.DoesNotExist:
        return HttpResponse(status=404)
    # step 2, use serializer to parse model data into dict 
    my_location_data = MyLocationUpdateSerializer(my_location_record).data
    # step 3, remove the restaurant or attraction id from list
    try:
        my_location_data[target].remove(target_id)
    except:
        return HttpResponseNotFound('Not found')
    # step 4, save updated record
    serializer = MyLocationUpdateSerializer(my_location_record, data=my_location_data)
    if serializer.is_valid():
        serializer.save()
    
    return HttpResponse(status=204)

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