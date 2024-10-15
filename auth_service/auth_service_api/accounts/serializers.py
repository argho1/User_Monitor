from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser, NotificationPreferences#, Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone_number')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # Accepts phone, email, or username
    password = serializers.CharField(write_only=True, required=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 
                  'username', 
                  'email', 
                  'phone_number', 
                  'is_active', 
                  'date_joined', 
                  'last_login', 
                  'is_superuser', 
                  'is_staff'
                ]


class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        fields = ['email_notification', 'sms_notification']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['permissions'] = list(user.get_all_permissions())
        token['groups'] = [group.name for group in user.groups.all()]

        return token