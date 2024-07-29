from django.urls import include, path

from rest_framework import routers

from appcomment import views

router = routers.DefaultRouter()
router.register(r'comments', views.CommentViewSet)  # api/comments/?user_id__id=<id> for filter by user
router.register(r'read_comment', views.ReadCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
