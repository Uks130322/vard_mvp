from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from appuser.views import RegisterView, GoogleLogin, GitHubLogin, FlatpageView, UserViewSet, AccessViewSet
from appuser.auth_router import DefaultRouterWithSimpleViews

from appchart_DB.urls import router as appchart_DBrouter
from appchat.urls import router as appchatrouter
from appcomment.urls import router as appcommentrouter
from appfeedback.urls import router as appfeedbackrouter
from appfile.urls import router as appfilerouter
from appuser.urls import router as appuserrouter


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser,),
)


router = DefaultRouterWithSimpleViews()
router.registry.extend(appchart_DBrouter.registry)
router.registry.extend(appchatrouter.registry)
router.registry.extend(appcommentrouter.registry)
router.registry.extend(appfeedbackrouter.registry)
router.registry.extend(appfilerouter.registry)
router.registry.extend(appuserrouter.registry)
router.register(r'register',RegisterView, basename="register")
router.register(r'login', LoginView, basename="login")
router.register(r'logout', LogoutView, basename="logout")
router.register(r'user', UserDetailsView, basename="user_details")
router.register(r'google_login', GoogleLogin, basename="google_login")
router.register(r'github_login', GitHubLogin, basename="github_login")

urlpatterns = [
    path('admin/', admin.site.urls), # нет в свагере
    path('api/accounts/', include('allauth.urls')), # нет в свагере

    path('api/', include(router.urls)),

    path('drf/', include('rest_framework.urls', namespace='rest_framework')), # нет в свагере # не работает путь
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # нет в свагере
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # нет в свагере
]
