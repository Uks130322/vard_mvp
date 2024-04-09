from django.urls import path, include
from rest_framework import routers
from appquery import views
from vardapp import views as views2


router = routers.DefaultRouter()
router.register(r'users', views2.UserViewset)
router.register(r'charts', views.ChartViewSet)
router.register(r'clientdb', views.ClientDBViewSet)
router.register(r'clientdata', views.ClientDataViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('drf/', include('rest_framework.urls', namespace='rest_framework')),
]
