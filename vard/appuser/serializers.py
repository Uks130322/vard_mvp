from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from appuser.models import User, Access


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

    def create(self, validated_data, **kwargs):
        try:
            querysets = Access.objects.filter(owner_id=validated_data['owner_id']).filter(
                user_id=validated_data['user_id'])
            for queryset in querysets:
                id = queryset.id
            if not querysets.exists() and validated_data['owner_id'] != validated_data['user_id']:
                access = Access.objects.create(**validated_data)
            else:
                access = Access.objects.get(id=id)
            return access
        except BaseException as error:
            raise ValidationError('You can not add access to yourself')
