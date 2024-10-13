import os
import requests
from django.conf import settings
from datetime import datetime
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def get_user_activity_data():
    headers = {
        'Authorization': f'Bearer {get_service_token()}'
    }
    response = requests.get(settings.AUTH_LIST_USERS_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print('\nAUTHENTICATON FAILED while getting user data!!\n')
        return None

def get_weather_data(location='New York'):
    api_key = settings.WEATHER_API_KEY
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print('\nAUTHENTICATON FAILED while getting Weather data!!\n')
        return None

def generate_pdf_report(user_data, weather_data=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add title to PDF
    pdf.setTitle('Daily Report')

    # User Activity Section
    pdf.drawString(50, height - 50, 'User Activity Report')
    y = height - 70
    for user in user_data:
        pdf.drawString(50, y, f"User ID: {user['id']}, Username: {user['username']}, Last Login: {user['last_login']}")
        y -= 20

    # if weather_data:
    #     # Weather data
    #     pdf.drawString(50, y-20, 'Weather Report')
    #     y -= 40
    #     pdf.drawString(50, y, f'Location: {weather_data['location']['name']}')
    #     pdf.drawString(50, y - 20, f"Temperature: {weather_data['current']['temp_c']} °C")

    # Finalize the PDF
    pdf.showPage()
    pdf.save()

    # Get the PDF data
    buffer.seek(0)

    return buffer.getvalue()

def get_service_token():
    data = {
        'identifier': settings.SERVICE_ACCOUNT_USERNAME,
        'password': settings.SERVICE_ACCOUNT_PASSWORD,
    }

    response = requests.post(settings.AUTH_LOGIN_URL, data=data)
    if response.status_code == 200:
        return response.json()['access']
    else:
        print(f'\nAUTHENTICATON FAILED while getting user data!!\n {response.status_code}')
        return None
    
def get_superusers_and_staff():
    auth_service_url = settings.AUTH_LIST_USERS_URL
    headers = {
        'Authorization': f'Bearer {get_service_token()}'
    }

    response = requests.get(auth_service_url, headers=headers, params={'is_staff': True})

    if response.status_code == 200:
        return response.json()
    else:
        return []

