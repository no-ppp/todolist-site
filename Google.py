import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# Ustawienie logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    if os.path.exists("token.json"):
        logger.info("Loading credentials from token.json")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired credentials")
            creds.refresh(Request())
        else:
            logger.info("Authorizing new credentials")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            # Ustawienie portu na 8000
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            logger.info("Saving credentials to token.json")
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            logger.info("No labels found.")
        else:
            logger.info("Labels:")
            for label in labels:
                logger.info(label["name"])
    except HttpError as error:
        logger.error(f"An error occurred: {error}")

if __name__ == "__main__":
    main()