from django.urls import path
from .views import ReportListView, ReportDetailView, GenerateReportView, ReportDownloadView

urlpatterns = [
    path('reports/generate/', GenerateReportView.as_view(), name='generate-report'),
    path('reports/history/', ReportListView.as_view(), name='report-list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('reports/<int:pk>/download/', ReportDownloadView.as_view(), name='report-download'),
]