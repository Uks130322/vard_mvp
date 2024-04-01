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
    user_url = serializers.URLField(source='load_by_url', write_only=True, allow_blank=True)

    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs = {
            'date_delete': {'read_only': True},
        }

    def load_by_url(self):
        pass  ######### TODO

    def create(self, validated_data):
        if validated_data['load_by_url']:
            return self.load_by_url

        validated_data.pop('load_by_url', None)
        file = File(**validated_data)
        file.name = file.link.name
        file.save()
        return file


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
