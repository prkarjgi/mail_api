from rest_framework import serializers

from schedules.models import Schedule, Recipient
from utils import validators


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['name', 'email_address']


class ScheduleSerializer(serializers.Serializer):
    recipients = RecipientSerializer(many=True)
    content = serializers.CharField(max_length=1000)
    frequency = serializers.DurationField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        """
        Check input fields for constraints
        """
        validators.start_date_after_today(data['start_date'])
        validators.start_date_before_end_date(
            data['start_date'], data['end_date']
        )
        validators.recipients_less_than_500(data['recipients'])
        validators.recipients_not_contains_duplicates(data['recipients'])
        return data

    def create(self, validated_data):
        pass
