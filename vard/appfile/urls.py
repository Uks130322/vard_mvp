from django.urls import include, path

from rest_framework import routers

from appfile import views

router = routers.DefaultRouter()
router.register(r'files', views.FileViewSet)  # api/files/?user_id__id=2 for filter by user with id=2

urlpatterns = [
    path('', include(router.urls)),
]
