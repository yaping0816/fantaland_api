from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('fantaland_app.urls'))
]
