import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_drive(user_email):
    token_file = f"token_{user_email}.pickle"

    creds = None

    # load existing token
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # if no token → login
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service


def upload_to_drive(file_path, user_email):
    try:
        service = authenticate_drive(user_email)

        file_name = os.path.basename(file_path)

        media = MediaFileUpload(file_path)

        service.files().create(
            body={'name': file_name},
            media_body=media
        ).execute()

        print(f"Uploaded to Drive: {file_name}")
        return True

    except Exception as e:
        import traceback
        print("Drive Upload Error:", e)
        traceback.print_exc()
        return False