import base64
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from django.conf import settings
from twilio.rest import Client
# import logging 

# logger = logging.getLogger('authentication')

def send_email(to_email, subject, content, attachment=None):
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )

    if attachment:
        encoded_file = base64.b64encode(attachment).decode('utf-8')
        attachment_file = Attachment(
            FileContent(encoded_file),
            FileName('Report.pdf'),
            FileType('application/pdf'),
            Disposition('attachment')
        )

        message.attachment = attachment_file

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        print(f"\n\nEmail sent to {to_email}\n\n")
    except Exception as e:
        print(f"\n\nError sending email:{e}\n\n")


def send_sms(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"\n\nSMS send to {to_number}\n\n")
    except Exception as e:
        print(f'\n\nError sending SMS: {e}\n\n')


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
    

def get_service_token():
    data = {
        'username': settings.SERVICE_ACCOUNT_USERNAME,
        'password': settings.SERVICE_ACCOUNT_PASSWORD,
    }

    response = requests.post(settings.AUTH_LOGIN_URL, data=data)
    if response.status_code == 200:
        # print(response.json()['access'])
        return response.json()['access']
    else:
        print(f'\nAUTHENTICATON FAILED while getting user data!!\n {response.status_code}')
        return None


def get_user_notification_perference(user_id):

    token = get_service_token()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'{settings.AUTH_SERVICE_URL}user/{user_id}/notification/', 
                                headers=headers, 
                                timeout=5)
        response.raise_for_status()
        perference = response.json()
        return perference
    except requests.RequestException as e:
        print(f'Failed to fetch perference : {requests.status_codes}')
        return None

