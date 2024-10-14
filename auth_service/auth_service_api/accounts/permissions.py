from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Fro admin access
        if request.user.is_staff or request.user.is_superuser:
            return True
        # For user access
        return obj.user == request.user