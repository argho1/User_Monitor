from django.urls import path

from .views import RegisterView, LoginView, ValidateTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('validate/', ValidateTokenView.as_view(), name='auth_validate')
]