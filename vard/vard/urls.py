from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from allauth.socialaccount.views import signup
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from appuser.views import RegisterView, GoogleLogin, GitHubLogin

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


router = routers.DefaultRouter()
router.registry.extend(appchart_DBrouter.registry)
router.registry.extend(appchatrouter.registry)
router.registry.extend(appcommentrouter.registry)
router.registry.extend(appfeedbackrouter.registry)
router.registry.extend(appfilerouter.registry)
router.registry.extend(appuserrouter.registry)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('allauth.urls')),
    path('api/', include(router.urls)),


    path('drf/', include('rest_framework.urls', namespace='rest_framework')),
    path("api/auth/login/", LoginView.as_view(), name="rest_login"),
    path("api/auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("api/auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("api/auth/signup/", signup, name="socialaccount_signup"),
    path("api/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path('api/auth/github/', GitHubLogin.as_view(), name='github_login'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

