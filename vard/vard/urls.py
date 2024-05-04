from django.contrib import admin
from django.urls import path, include, re_path
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from allauth.socialaccount.views import signup
from vardapp.views import GoogleLogin, GitHubLogin, RegisterView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



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
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include('APIapp.urls')),

    path("auth/register/", RegisterView.as_view(), name="rest_register"),
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("auth/signup/", signup, name="socialaccount_signup"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path('auth/github/', GitHubLogin.as_view(), name='github_login'),

    path('swagger/',schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc'),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('allauth.urls')),
#     path('api/', include('APIapp.urls')),
#
#     path("auth/register/", RegisterView.as_view(), name="rest_register"),
#     path("auth/login/", LoginView.as_view(), name="rest_login"),
#     path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
#     path("auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
#     path("auth/signup/", signup, name="socialaccount_signup"),
#     path("auth/google/", GoogleLogin.as_view(), name="google_login"),
#     path('auth/github/', GitHubLogin.as_view(), name='github_login')
# ]
