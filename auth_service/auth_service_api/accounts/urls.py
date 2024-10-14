from django.urls import path

from .views import RegisterView, ValidateTokenView, CustomUserListView, UpdateNotificationPreferencesView , CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    # path('login/', LoginView.as_view(), name='auth_login'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('validate/', ValidateTokenView.as_view(), name='auth_validate'),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('user/<int:pk>/notification/', UpdateNotificationPreferencesView.as_view(), name='update_notification_preferences'),
]