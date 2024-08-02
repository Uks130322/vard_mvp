from django.urls import include, path
from rest_framework import routers
from appuser import views



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'access', views.AccessViewSet)
router.register(r'authregister', views.RegisterView, basename='authregister')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', views.FlatpageView, name= 'FlatpageView'),

]

