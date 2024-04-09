from django.urls import include, path
from rest_framework import routers

from APIapp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, )
router.register(r'access', views.AccessViewSet)
router.register(r'files', views.FileViewSet)
router.register(r'filesuser', views.FileUserViewSet, basename='filesuser')
router.register(r'commentuser', views.CommentUserViewSet, basename='commentuser')
router.register(r'dashboarduser', views.DashboardUserViewSet, basename='dashboarduser')
router.register(r'chartuser', views.ChartUserViewSet, basename='chartuser')
router.register(r'feedback', views.FeedbackViewSet)
router.register(r'dashboards', views.DashboardViewSet)
router.register(r'charts', views.ChartViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'read_comment', views.ReadCommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
