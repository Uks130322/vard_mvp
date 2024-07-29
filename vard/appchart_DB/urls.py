from appchart_DB import views

from django.urls import include, path

from rest_framework import routers

from appchart_DB import views as DBviews

router = routers.DefaultRouter()
router.register(r'dashboards', views.DashboardViewSet)  # api/dashboards/?user_id__id=<id> for filter by user
router.register(r'charts', views.ChartViewSet)  # api/charts/?user_id__id=<id> for filter by user
router.register(r'clientdb', DBviews.ClientDBViewSet)
router.register(r'clientdata', DBviews.ClientDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


