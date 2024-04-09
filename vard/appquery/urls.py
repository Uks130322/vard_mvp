from django.urls import path, include
from rest_framework import routers
from appquery import views


router = routers.DefaultRouter()
router.register(r'clientdb', views.ClientDBViewSet)
router.register(r'clientdata', views.ClientDataViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('drf/', include('rest_framework.urls', namespace='rest_framework')),
]
