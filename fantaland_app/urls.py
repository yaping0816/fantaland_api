from django.urls import path
from .views import current_user, UserList
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_jwt_token),
    path('current_user/', current_user), # get user info by token
    path('users/', UserList.as_view()) # sign up
]