from rest_framework import serializers

from vardapp.models import *
from APIapp.utils import load_csv, load_json


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'is_superuser',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
        }


class AccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Access
        fields = '__all__'
        extra_kwargs = {
            'owner_id': {'read_only': True},
        }


class FileSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.URLField(source='load_by_url', write_only=True, allow_blank=True)

    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs = {
            'date_delete': {'read_only': True},
            'user_id': {'read_only': True},
            'type_id': {'read_only': True},
        }

    def load_by_url(self, validated_data):
        try:
            validated_data = load_json(self, validated_data)
            return validated_data
        except BaseException as error:
            print(error)
            try:
                validated_data = load_csv(self, validated_data)
                return validated_data
            except BaseException as error:
                print(error)
                return validated_data

    def create(self, validated_data):
        if validated_data['load_by_url']:
            validated_data = self.load_by_url(validated_data)

        validated_data.pop('load_by_url', None)
        file = File(**validated_data)
        if not file.name:
            file.name = file.link.name
        file_type = file.link.name.split('.')[-1].upper()
        file.type_id = File.FilesType[file_type].value
        file.save()
        return file


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class DashboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class ChartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chart
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }


class ReadCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadComment
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }
