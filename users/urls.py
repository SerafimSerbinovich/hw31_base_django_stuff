from django.urls import path
from rest_framework import routers
from users.views import *

location_router = routers.SimpleRouter()
location_router.register('location', LocationViewSet)

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
]

urlpatterns += location_router.urls
