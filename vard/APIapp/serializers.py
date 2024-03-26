from vardapp.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_superuser', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Access
        fields = '__all__'


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class DashboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'


class ChartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chart
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReadCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadComment
        fields = '__all__'
