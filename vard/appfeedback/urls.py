from django.urls import include, path

from rest_framework import routers

from appfeedback import views

router = routers.DefaultRouter()
router.register(
    r'feedback', views.FeedbackViewSet, basename='feedback'
)


urlpatterns = router.urls
