from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from allauth.socialaccount.views import signup
from vardapp.views import GoogleLogin, GitHubLogin, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include('APIapp.urls')),

    path("auth/register/", RegisterView.as_view(), name="rest_register"),
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("auth/signup/", signup, name="socialaccount_signup"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path('auth/github/', GitHubLogin.as_view(), name='github_login')
]
