from rest_framework import serializers
from vardapp.models import *
from appchat.models import Chat
from appquery.serializers import ClientDataSerializer
from APIapp.utils import load_csv, load_json
from drf_writable_nested import WritableNestedModelSerializer


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
        fields = ['id','user_id','date_creation','date_change','clientdb_id','str_query','clientdata']
        extra_kwargs = {
            'user_id': {'read_only': True},
            'clientdata': {'read_only': True},
        }

    # def update(self, instance, validated_data):
    #     clientdata = validated_data.pop('clientdata')
    #     clientdata = ClientData.objects.update(**clientdata)
    #     return super().update(instance, validated_data)

    def create(self, validated_data, **kwargs):
        #print('validated_data',validated_data)
        clientdata = ClientData.objects.create(user_id=validated_data['user_id'],data='')
        chart = Chart.objects.create(**validated_data, clientdata = clientdata)
        #print('chart',clientdata.chart.id)
        return chart

#select * from vardapp_users


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


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chat
        fields = [
            'id',
            'user_id_owner',
            'user_id_sender',
            'date_send',
            'date_remove',
            'is_remove',
            'message'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'user_id_owner': {'read_only': True},
            'user_id_sender': {'read_only': True},
        }


class ChartDashboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChartDashboard
        fields = '__all__'