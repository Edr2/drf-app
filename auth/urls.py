from django.urls import path
from .views import LoginView, RegisterUsersView
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('login/', LoginView.as_view(), name="auth-login"),
    path('register/', RegisterUsersView.as_view(), name="auth-register"),
    path('token-refresh/', refresh_jwt_token, name="auth-token-refresh")
]
