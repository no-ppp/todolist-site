import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(BASE_DIR, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=8001)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)
    raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, user_id, message):
    try:
        send_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')

def sendingMessage(sender, recipient, subject, message_text):
    service = get_service()
    user_id = 'me'
    message = create_message(sender, recipient, subject, message_text)
    send_message(service, user_id, message)

def main():
    sendingMessage(
        sender='your-email@gmail.com',
        recipient='recipient-email@example.com',
        subject='Test Email',
        message_text='This is a test email sent from the Gmail API.'
    )

if __name__ == "__main__":
    main()