from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import time

SERVICE_ACCOUNT_FILE = 'service-account-key.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def file_exists(service, folder_id, filename):
    query = f"'{folder_id}' in parents and name = '{filename}' and trashed = false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = results.get('files', [])
    return files[0] if files else None


def upload_or_replace_file(service, file_path, folder_id, existing_file=None):
    filename = os.path.basename(file_path)
    
    if existing_file:
        # Check if the file was modified within the last week
        one_week_ago = time.time() - (7 * 24 * 60 * 60)
        if os.path.getmtime(file_path) > one_week_ago:
            print(f"File '{filename}' exists and was modified within the last week, replacing it.")
            file_id = existing_file['id']
            media = MediaFileUpload(file_path, resumable=True)
            updated_file = service.files().update(fileId=file_id, media_body=media).execute()
            print(f"Replaced File ID: {updated_file.get('id')}")
        else:
            print(f"File '{filename}' exists but was not modified within the last week, skipping.")
    else:
        print(f"Uploading new file '{filename}'.")
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        new_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded File ID: {new_file.get('id')}")

def main():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    folder_to_backup = '/data'
    folder_id = os.environ.get('FOLDER_ID')

    for filename in os.listdir(folder_to_backup):
        file_path = os.path.join(folder_to_backup, filename)

        if os.path.isfile(file_path):
            existing_file = file_exists(service, folder_id, filename)
            upload_or_replace_file(service, file_path, folder_id, existing_file)

if __name__ == '__main__':
    main()
