from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied
from .models import Report
import requests
from django.conf import settings
import jwt

class HasReportAccessPermission(BasePermission):
    """
    Custom permission to check if a user has access to generate/view reports.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        # Extract token
        token = auth_header.split(' ')[1]

        payload = jwt.decode(token,options={"verify_signature": False}, algorithms=['HS256'])

        permissions = payload.get('permissions', [])

        # Checking if 'accounts.view_report' permission is in the token
        if 'accounts.view_report' in permissions:
            return True
        else:
            raise PermissionDenied("You do not have access to this resource!")



class IsTokenValid(BasePermission):
    """
    Custom permission to check if the JWT token is valid by sending it to a third-party service.
    """

    def has_permission(self, request, view):
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        
        # Checking Authorization header is present and is a Bearer token
        if not auth_header or not auth_header.startswith('Bearer '):
            return False  # No token or wrong format, deny access

        # Extract token
        token = auth_header.split(' ')[1]
        
        # Validate token with the external service
        url = settings.AUTH_VALIDATE_URL
        headers = {'Authorization': f'Bearer {token}'}

        try:
            # Makeing request to the /validate endpoint
            validation_response = requests.get(url, headers=headers)

            if validation_response.status_code == 200:
                return True
            else:
                raise PermissionDenied("Token is invalid or expired.")

        except requests.exceptions.RequestException:
            raise PermissionDenied("Error while contacting the authentication service.")