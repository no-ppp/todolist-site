import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables (not used here, but good practice)
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

BASE_DIR = Path(__file__).resolve().parent
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_service():
    creds = None
    token_path = BASE_DIR / 'token.json'
    credentials_path = BASE_DIR / 'credentials.json'

    # Check if token file exists
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        print("Loaded credentials from file.")
    
    # Refresh or get new credentials if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("Token refreshed.")
            except Exception as e:
                print(f'Error refreshing token: {e}')
                creds = None  # Force re-authentication
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=8080)
            print("New token obtained.")
        
        # Save the new credentials to the file
        with token_path.open('w') as token_file:
            token_file.write(creds.to_json())
            print("Token saved to file.")

    try:
        service = build('gmail', 'v1', credentials=creds)
        print("Gmail service created successfully.")
        return service
    except Exception as e:
        print(f'Error creating service: {e}')
        return None

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

def sending_message(sender, to, subject, message_text):
    service = get_service()
    user_id = 'me'
    message = create_message(sender, to, subject, message_text)
    send_message(service, user_id, message)