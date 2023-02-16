import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers


def check_birth_date(value):
    age = relativedelta(datetime.date.today(), value).years
    if age < 9:
        raise serializers.ValidationError('Возраст должен быть более 9 лет')


def check_email_address(value):
    if value.endswith("@rambler.ru"):
        raise serializers.ValidationError('Почта должна быть зарегистрирована не на rambler.ru')
