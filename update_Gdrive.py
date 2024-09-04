from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
import re

# !wget '' -O credentials.json -q

# have to download the credentials.json file from the google cloud platform
# Replace with the path to your service account key file
KEY_FILE_LOCATION = 'credentials.json'

# Authenticate using the service account key file
creds = Credentials.from_service_account_file(KEY_FILE_LOCATION, scopes=['https://www.googleapis.com/auth/drive'])

# Build the Drive API client
service = build('drive', 'v3', credentials=creds)


# Function to update the ngrok link in the Google Drive file(example)
def update_ngrok(ngrok_link):
  # Specify the new link
  # Use regular expression pattern to extract ngrok link
  pattern = r'"(https?://[^"]+)"'
  match = re.search(pattern, ngrok_link)

  if match:
      ngrok_link = match.group(1)
      print("Extracted ngrok link:", ngrok_link)
      new_link = ngrok_link
  else:
      print("Ngrok link not found in the text.")


  # Replace with the ID of the file you want to write to
  file_id = ''

  try:
      # Create a file-like object containing the data to write
      file_data = BytesIO(ngrok_link.encode('utf-8'))

      # Create a media upload object
      media = MediaIoBaseUpload(file_data, mimetype='text/plain', resumable=True)

      # Update the file on Google Drive
      service.files().update(fileId=file_id, media_body=media, fields='id').execute()
      return 'File updated'
  except HttpError as error:
      print(f'An error occurred: {error}')