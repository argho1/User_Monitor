from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied
from .models import Report

class HasReportAccessPermission(BasePermission):
    """
    Custom permission to check if a user has access to generate/view reports.
    """

    def has_permission(self, request, view):
        auth = JWTAuthentication()
        print(auth)
        try:
            user, token = auth.authenticate(request)
            print(token)
        except Exception as e:
            print(e)
            return False

        permissions = token.payload.get('permissions', [])

        if 'accounts.view_customuser' in permissions:
            return True
        elif 'app_label.view_team_reports' in permissions:
            return self._is_report_in_user_team(request, view, user)
        elif 'app_label.view_own_reports' in permissions:
            return self._is_report_owned_by_user(request, view, user)
        else:
            return False

    def _is_report_in_user_team(self, request, view, user):
        """
        Check if the report belongs to the user's team.
        Implement the logic based on your team and report models.
        """
        report_id = request.data.get('report_id')  # Assuming report_id is sent in the request
        if not report_id:
            return False

        try:
            report = view.get_report(report_id)
        except Report.DoesNotExist:
            return False

        # Assuming Report model has a team field and User has a team relation
        return report.team == user.team

    def _is_report_owned_by_user(self, request, view, user):
        """
        Check if the report is owned by the user.
        Implement the logic based on your user and report models.
        """
        report_id = request.data.get('report_id')  # Assuming report_id is sent in the request
        if not report_id:
            return False

        try:
            report = view.get_report(report_id)
        except Report.DoesNotExist:
            return False

        return report.owner == user