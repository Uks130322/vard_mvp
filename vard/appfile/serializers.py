from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from appfile.hash_md import get_hash_md5
from appfile.models import File
from appfile.utils import load_json, load_csv
from vard import settings


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
            try:
                validated_data = load_csv(self, validated_data)
                return validated_data
            except BaseException as error:
                raise ValidationError(error)

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

        path_instance = f'{settings.BASE_DIR}{settings.MEDIA_URL}files/{file.link}'.replace('\\', '/')
        hash_instance = get_hash_md5(path_instance)
        files = File.objects.filter(user_id=validated_data['user_id']).exclude(id=file.id)

        for file_ in files:
            path_file = f'{settings.BASE_DIR}{settings.MEDIA_URL}files/{file_.link}'.replace('\\', '/')
            hash_file = get_hash_md5(path_file)
            if hash_instance == hash_file:
                file.link.delete()
                file.delete()
                file = file_
        return file
