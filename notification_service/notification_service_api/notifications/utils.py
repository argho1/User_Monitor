from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from twilio.rest import Client

def send_email(to_email, subject, content):
    message = Mail(
        from_email="sinhaargho@gmail.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email:{e}")


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