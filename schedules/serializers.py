from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import EmailValidator

from schedules.models import Schedule, Recipient
from utils import validators
from utils.serializers import create_or_update_recipients


class RecipientSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email_address = serializers.EmailField(
        required=True, validators=[EmailValidator]
    )

    def create(self, validated_data):
        return Recipient.objects.create(**validated_data)


class ScheduleSerializer(serializers.Serializer):
    description = serializers.CharField()
    subject = serializers.CharField(required=True)
    recipients = RecipientSerializer(many=True)
    content = serializers.CharField(required=True, max_length=1000)
    frequency = serializers.DurationField(required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Schedule.objects.all(),
                fields=[
                    'description', 'subject', 'content',
                    'frequency', 'start_date', 'end_date'
                ],
                message=validators.FIELDS_NOT_UNIQUE_TOGETHER_ERROR
            )
        ]

    def validate(self, data):
        """
        Check input fields for constraints
        """
        validators.start_date_after_today(data['start_date'])
        validators.start_date_before_end_date(
            data['start_date'], data['end_date']
        )
        validators.frequency_not_greater_than_end_date(
            data['frequency'], data['start_date'], data['end_date']
        )
        validators.recipients_less_than_500(data['recipients'])
        validators.recipients_not_contains_duplicates(data['recipients'])

        return data

    def create(self, validated_data):
        schedule = Schedule.objects.create(
            description=validated_data['description'],
            subject=validated_data['subject'],
            content=validated_data['content'],
            frequency=validated_data['frequency'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date']
        )
        recipients = validated_data['recipients']
        create_or_update_recipients(schedule, recipients, False)
        return schedule

    def update(self, instance, validated_data):
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.subject = validated_data.get(
            'subject', instance.subject
        )
        instance.content = validated_data.get(
            'content', instance.content
        )
        instance.frequency = validated_data.get(
            'frequency', instance.frequency
        )
        instance.start_date = validated_data.get(
            'start_date', instance.start_date
        )
        instance.end_date = validated_data.get(
            'end_date', instance.end_date
        )
        recipients = validated_data.get('recipients')
        if recipients:
            create_or_update_recipients(instance, recipients, True)
        instance.status = instance.status
        instance.save()
        return instance
