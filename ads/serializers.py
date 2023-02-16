from ads.models import Ad, Category, Selection
from ads.validators import not_null
from rest_framework import serializers
from users.serializers import UserSerializer, UserLocationSerializer


class AdSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[not_null], required=False)
    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    author = UserLocationSerializer()

    class Meta:
        model = Ad
        fields = ['name', 'price', 'author', 'category']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'

