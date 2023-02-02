from django.db.models import Count, Q
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from users.serializers import *


class UserPagination(PageNumberPagination):
    page_size = 6


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')
    pagination_class = UserPagination


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserDeleteView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
