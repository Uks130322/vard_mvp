from rest_framework import serializers

from appfeedback.models import Feedback


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
        }