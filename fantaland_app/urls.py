from django.urls import path
# from .views import current_user, UserList
from rest_framework_jwt.views import obtain_jwt_token
# from django.contrib import admin
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # outside api proxy routes
    path('city_info/', city_info ), # get city detailed info
    path('attractions_count/', attractions_count), # get attractions count by city name
    # path('attractions_list/', attractions_list),
    # path('attraction_detail/<int:id>/', attraction_detail),
    # path('restaurants_list/', restaurants_list), # get restaurants list by location
    # path('restaurant_detail/<int:id>/', restaurant_detail), # get restaurant detail by id

    path('list/<target>/', process_lists),
    path('detail/<target>/<id>/', process_detail),

    path('weather_info/', weather_info), # get weather info
    # internal api routes
    path('login/', obtain_jwt_token), #log in
    path('current_user/', current_user), # get user info by token
    path('signup/', UserList.as_view()), # sign up
    path('favorite/', favorite), # add a MyLocation record
    path('favorite/<int:my_location_id>/<target>/', add_restaurant_or_attraction_to_favorite),
    path('favorite/<int:my_location_id>/<target>/<int:target_id>/', remove_restaurant_or_attraction_from_favorite),
]

router = DefaultRouter()
# router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
# router.register(r'attractions', AttractionViewSet, basename='attractions')
# router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'my_locations', MyLocationViewSet, basename='my_locations')

urlpatterns += router.urls

