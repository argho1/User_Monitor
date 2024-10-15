import logging
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from auth_service_api.rabbitmq_publisher import RabbitMQPublisher

# from .utils import authenticate_with_multiple_fields
from .permissions import IsAdminOrOwner
from .models import CustomUser, NotificationPreferences
from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer, NotificationPreferencesSerializer, CustomTokenObtainPairSerializer


logger = logging.getLogger(__name__)

# To prevent brute-force or abuse
class BurstRateThrottle(UserRateThrottle):
    rate = '5/min'


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    throttle_classes = [BurstRateThrottle]

    @transaction.atomic # to ensure atomic db transactions
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                # publisher = RabbitMQPublisher()
                message = {
                    'user_id' : user.id,
                    'phone_number': user.phone_number,
                    'email' : user.email,
                    'username' : user.username,
                }
                with RabbitMQPublisher(queue_name='user_registered') as publisher:
                    publisher.publish(message)

            except Exception as e:
                logger.error(f"Error publishing to RabbitMQ: {e}")
                # comment out below lines if publishing is not critical
                transaction.set_rollback(True)
                return Response({'detail': 'Registration failed. Please try again later.'}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'detail': 'User registered successfully'}, 
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     throttle_classes = [BurstRateThrottle]

#     def post(self, requset):
#         serializer = self.get_serializer(data=requset.data)
#         serializer.is_valid(raise_exception=True)
    
#         identifier = serializer.validated_data['identifier']  
#         password = serializer.validated_data['password']

#         user = authenticate_with_multiple_fields(identifier, password)
    
#         if user:
#             refresh = RefreshToken.for_user(user)
#             # Create the Response instance first
#             response = Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#             return response
        
#         return Response({
#             'detail':'Invalid Credentials'
#         }, status=status.HTTP_401_UNAUTHORIZED)


class ValidateTokenView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # roles = [role.name for role in user.roles.all()]
        permissions = list(user.get_all_permissions())
        return Response({
            'detail': 'Token is valid',
            'user_id': user.id,
            # 'roles': roles,
            'permissions': permissions
        }, status=200)


class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'is_staff': ['exact'],  # Filtering by exact match for 'is_staff'
        'is_active': ['exact'],  # Filtering by exact match for 'is_staff'
        'date_joined': ['gte', 'lte'],  # Filtering by date range (greater than, less than)
        'last_login': ['gte', 'lte', 'isnull'],  # Filtering by last login range
    }


class UpdateNotificationPreferencesView(generics.RetrieveUpdateAPIView):
    queryset = NotificationPreferences.objects.all()
    serializer_class = NotificationPreferencesSerializer
    permission_classes = [AllowAny, IsAdminOrOwner]

    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get('pk')

        if user.is_staff or user.is_superuser:
            # Admins can access any user's preferences
            try:
                return NotificationPreferences.objects.get(user__pk=pk)
            except NotificationPreferences.DoesNotExist:
                raise PermissionDenied("Notification preferences not found for this user.")
        else:
            # Regular users can only access their own preferences
            if pk and int(pk) != user.pk:
                raise PermissionDenied("You do not have permission to access this object.")
            try:
                return NotificationPreferences.objects.get(user=user)
            except NotificationPreferences.DoesNotExist:
                raise PermissionDenied("Notification preferences not found for this user.")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # throttle_classes = [BurstRateThrottle]
