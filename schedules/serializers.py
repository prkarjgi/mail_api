from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from schedules.models import Schedule, Recipient
from utils import validators


class RecipientSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email_address = serializers.EmailField(required=True)

    def create(self, validated_data):
        return Recipient.objects.create(**validated_data)

    # class Meta:
    #     # validators = []
    #     model = Recipient
    #     fields = ['name', 'email_address']


class ScheduleSerializer(serializers.Serializer):
    recipients = RecipientSerializer(many=True)
    content = serializers.CharField(required=True, max_length=1000)
    frequency = serializers.DurationField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Schedule.objects.all(),
                fields=['content', 'frequency', 'start_date', 'end_date'],
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
        validators.recipients_less_than_500(data['recipients'])
        validators.recipients_not_contains_duplicates(data['recipients'])

        # validate = validators.RecipientDuplicateValidator()
        # validate(data['recipients'])
        return data

    def create(self, validated_data):
        schedule = Schedule.objects.create(
            content=validated_data['content'],
            frequency=validated_data['frequency'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date']
        )
        for recipient in validated_data['recipients']:
            if not Recipient.objects.filter(
                email_address=recipient['email_address']
            ).exists():
                print('not in db')
                recip = Recipient.objects.create(
                    name=recipient['name'],
                    email_address=recipient['email_address']
                )
                schedule.recipients.add(recip)
            else:
                print('already found')
                r = Recipient.objects.get(
                    email_address=recipient['email_address']
                )
                schedule.recipients.add(r)
        return schedule

    def update(self, instance, validated_data):
        return instance
