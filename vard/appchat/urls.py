from django.urls import include, path

from rest_framework import routers

from appchat import views

router = routers.DefaultRouter()

router.register(r'chat', views.ChatViewSet, basename='chat')
router.register(r'message', views.MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
