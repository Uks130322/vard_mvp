from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from allauth.account.utils import complete_signup
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, RegisterView
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.serializers import TokenSerializer

from appuser.models import Access, User
from appuser.serializers import UserSerializer, AccessSerializer


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



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed
    """
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Superuser can see all users, others can see only themselves"""
        if self.request.user.is_superuser:
            queryset = User.objects.all().order_by('name')
        else:
            queryset = User.objects.filter(email=self.request.user)  # one authorized user
        return queryset


class AccessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Access to be viewed or edited. Only Owner can change access level.
    """
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
    filterset_fields = ['user_id__id', 'owner_id__id']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """The creator is automatically assigned as owner_id"""
        if serializer.validated_data['user_id']:
            datas = serializer.validated_data
            return Response(serializer.save(owner_id=self.request.user, **datas), status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """Superuser can see all access, others can see only theirs own"""
        if self.request.user.is_superuser:
            queryset = Access.objects.all()
        else:
            queryset = Access.objects.filter(owner_id=self.request.user)
        return queryset
