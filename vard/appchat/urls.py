from django.urls import include, path

from rest_framework import routers

from appchat import views

router = routers.DefaultRouter()

router.register(r'chat', views.ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]
