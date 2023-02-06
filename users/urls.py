from django.urls import path
from rest_framework import routers
from users.views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
location_router = routers.SimpleRouter()
location_router.register('location', LocationViewSet)

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]

urlpatterns += location_router.urls
