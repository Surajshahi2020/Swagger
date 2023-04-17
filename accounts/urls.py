from django.urls import path, include
from accounts.api.viewsets.accounts import (
    UserCreateView,
    UserListView,
    UserDeleteView,
    UserUpdateView,
    UserDetailView,
    EmailLoginView,
    CustomTokenRefreshView,
)

from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("user-create/", UserCreateView.as_view()),
    path("user-list/", UserListView.as_view()),
    path("user-detail/<int:pk>", UserDetailView.as_view()),
    path("user-delete/<int:pk>/", UserDeleteView.as_view()),
    path("user-update/<int:pk>/", UserUpdateView.as_view()),
    path("user-login/", EmailLoginView.as_view()),
    path("refresh/", CustomTokenRefreshView.as_view()),
]
