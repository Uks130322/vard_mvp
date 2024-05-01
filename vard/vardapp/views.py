from allauth.account.utils import complete_signup
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, RegisterView
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.serializers import TokenSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://natalietkachuk.pythonanywhere.com/api/"  # TODO clarify later
    client_class = OAuth2Client


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "https://natalietkachuk.pythonanywhere.com/api/"  # TODO clarify later
    client_class = OAuth2Client


class RegisterView(RegisterView):
    def get_response_data(self, user):
        return TokenSerializer(user.auth_token, context=self.get_serializer_context()).data, \
               {
                   'username': self.request.data['username'],
                   'email': self.request.data['email'],
               }

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        api_settings.TOKEN_CREATOR(self.token_model, user, serializer)

        complete_signup(
            self.request,
            user,
            None,
            None,
        )
        return user
