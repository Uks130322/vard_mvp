from django.urls import include, path
from rest_framework import routers
from appinvite import views

router = routers.DefaultRouter()

router.register(r'invite', views.InviteViewSet, basename='invite')

urlpatterns = [
    path('', include(router.urls)),
]
