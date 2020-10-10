from rest_framework import serializers

from schedules.models import Schedule, Recipient


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['name', 'email_address']


class ScheduleSerializer(serializers.ModelSerializer):
    recipients = RecipientSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'content', 'frequency', 'start_date', 'end_date', 'frequency'
        ]
