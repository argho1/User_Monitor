import base64
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from django.conf import settings
from twilio.rest import Client

def send_email(to_email, subject, content, attachment=None):
    message = Mail(
        from_email="sinhaargho@gmail.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )

    if attachment:
        encoded_file = base64.b64encode(attachment).decode('utf-8')
        attachment_file = Attachment(
            FileContent(encoded_file),
            FileName('report.pdf'),
            FileType('application/pdf'),
            Disposition('attachment')
        )

        message.attachment = attachment_file

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        print(f"\nEmail sent to {to_email}\n")
    except Exception as e:
        print(f"\nError sending email:{e}\n")


def send_sms(to_number, message):
    client = Client(settings.TWILO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"SMS send to {to_number}")
    except Exception as e:
        print(f'Error sending SMS: {e}')


def get_report_file(report_id):
    report_service_url = f'{settings.REPORTING_API_URL}{report_id}/download/'

    try:
        response = requests.get(report_service_url)
        if response.status_code == 200:
            return response.content
        else:
            print(f'Failed to fetch report : {response.status_code}')
            return None
    except Exception as e:
        print(f'Error fetching report:{e}')
        return None
