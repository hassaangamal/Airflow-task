from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from simulators.views import  calculate_kpi  

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/calculate-kpi/', calculate_kpi, name='calculate-kpi'),
]