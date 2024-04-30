from dj_rest_auth.views import UserDetailsView
from django.urls import include, path
from rest_framework import routers

from APIapp import views
from appquery import views as DBviews

router = routers.DefaultRouter()
router.register(r'clientdb', DBviews.ClientDBViewSet)
router.register(r'clientdata', DBviews.ClientDataViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'access', views.AccessViewSet)
router.register(r'files', views.FileViewSet)  # api/files/?user_id__id=2 for filter by user with id=2
router.register(r'feedback', views.FeedbackViewSet)
router.register(r'dashboards', views.DashboardViewSet)  # api/dashboards/?user_id__id=<id> for filter by user
# router.register(r'chartdashboard', views.ChartDashboardViewSet, basename='chartdashboard')
router.register(r'charts', views.ChartViewSet)  # api/charts/?user_id__id=<id> for filter by user
router.register(r'comments', views.CommentViewSet)  # api/comments/?user_id__id=<id> for filter by user
router.register(r'read_comment', views.ReadCommentViewSet)
router.register(r'chat', views.ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
    path('drf/', include('rest_framework.urls', namespace='rest_framework')),
]
