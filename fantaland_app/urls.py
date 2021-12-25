from django.urls import path
# from .views import current_user, UserList
from rest_framework_jwt.views import obtain_jwt_token
# from django.contrib import admin
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('login/', obtain_jwt_token), #log in
    path('current_user/', current_user), # get user info by token
    path('signup/', UserList.as_view()), # sign up
    path('city_info', city_info ), # get city detailed info
    path('attractions_count', attractions_count_by_city), # get attractions count by city name
    path('attractions_list', attractions_list_by_city),
    path('attraction_detail/<xid>/', attraction_detail),
]

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
router.register(r'attractions', AttractionViewSet, basename='attractions')
router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'locationlists', LocationListViewSet, basename='location_lists')

urlpatterns += router.urls

