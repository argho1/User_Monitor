from django.urls import path

from .views import RegisterView, LoginView, ValidateTokenView, CustomUserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('validate/', ValidateTokenView.as_view(), name='auth_validate')
]