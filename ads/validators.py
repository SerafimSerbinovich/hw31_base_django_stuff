from rest_framework import serializers


def not_null(value):
    if value:
        raise serializers.ValidationError('Значение не может быть True')