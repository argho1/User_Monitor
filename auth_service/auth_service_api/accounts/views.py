import logging
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle
from .serializers import RegisterSerializer, LoginSerializer
from auth_service_api.rabbitmq_publisher import RabbitMQPublisher

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
                publisher = RabbitMQPublisher()
                message = {
                    'user_id' : user.id,
                    'email' : user.email,
                    'username' : user.username,
                    'phone_number': user.phone_number,
                }
                publisher.publish(message)
                publisher.close()
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

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, requset):
        serializer = self.get_serializer(data=requset.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username = serializer.validated_data['username'],
            password = serializer.validated_data['password'],
            phone_number = serializer.validated_data['phone_number'],
        )

        if user:
            refresh = RefreshToken.for_user(user)
            # Create the Response instance first
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
            ##COOKITE based auth if needed
            ##Set the cookie on the Response instance
            # response.set_cookie(key='jwt',
            #                     value=str(refresh.access_token), 
            #                     httponly=True)
            return response
        
        return Response({
            'detail':'Invalid Credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class ValidateTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'detail':'Token is valid'},
                        status=status.HTTP_200_OK)