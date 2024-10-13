from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Report
from .serializers import ReportSerializer
from report_service_api.rabbitmq_publisher import RabbitMQPublisher
from .utils import get_user_activity_data, generate_pdf_report
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from datetime import datetime
from django.core.files.base import ContentFile

class GenerateReportView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = get_user_activity_data()
        pdf_buffer = generate_pdf_report(user_data)

        report = Report(title='User Data Report')
        # Get current date and time
        current_datetime = datetime.now()

        # Format it for a filename (e.g., 2024-10-11_15-43-22)
        filename_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        # Now you can use it as part of a filename
        filename = f"report_{filename_datetime}.pdf"
        report.file.save(filename, ContentFile(pdf_buffer))
        report.save()

        message = {
            'name': 'report_generated',
            'report_id': report.id,
            # 'generated_at': str(datetime.now()),
            'email': 'argho1@live.com',
            'report_type': 'daily_summary',
            'status': 'success',
        }
        with RabbitMQPublisher(queue_name='report_generated') as publisher:
            publisher.publish(message)
        return Response({'detail':'Generating report and sending email'},
                        status=status.HTTP_202_ACCEPTED)


class ReportListView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]


class ReportDetailView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]
    

class ReportDownloadView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        if not report.file:
            raise Http404("Report file not found!")
        response = HttpResponse(report.file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={report.title}.pdf'
        return response




