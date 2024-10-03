import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
from datetime import datetime

# Define the scope for accessing Google Photos
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

# Path to your credentials.json (downloaded from Google Cloud Console)
CREDENTIALS_FILE = 'credentials.json'

def authenticate_google_photos():
    """Authenticate and return a Google Photos service instance."""
    creds = None

    # Check if token.json exists (it stores the user's access and refresh tokens)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no valid credentials, go through the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the service using the discovery document for Google Photos API
    service = googleapiclient.discovery.build(
        'photoslibrary', 
        'v1', 
        credentials=creds,
        discoveryServiceUrl='https://photoslibrary.googleapis.com/$discovery/rest?version=v1'
    )

    return service

def parse_creation_time(creation_time):
    """Parse the creation time, handling cases with and without fractional seconds."""
    try:
        # Try parsing with fractional seconds
        return datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
    except ValueError:
        # If fractional seconds are not present, parse without them
        return datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d")

def list_photos_and_videos(service):
    """List and download photos and videos from Google Photos, handling pagination."""
    next_page_token = None
    total_items_downloaded = 0

    while True:
        try:
            # Fetch media items with pagination
            results = service.mediaItems().list(
                pageSize=100, pageToken=next_page_token).execute()
            items = results.get('mediaItems', [])
            next_page_token = results.get('nextPageToken')

            if not items:
                print("No items found.")
                break

            # Loop through media items and download each one
            for item in items:
                media_url = item['baseUrl']
                filename = item['filename']
                media_metadata = item.get('mediaMetadata', {})
                creation_time = media_metadata.get('creationTime', None)

                # If creation time is available, use it to create folder structure
                if creation_time:
                    creation_date = parse_creation_time(creation_time)
                else:
                    # Fallback in case creation time is not available
                    creation_date = "unknown_date"

                # Download the media and organize by date
                download_media(media_url, filename, creation_date)

                total_items_downloaded += 1

            print(f"Downloaded {total_items_downloaded} items so far...")

            # Exit loop if there are no more pages to fetch
            if not next_page_token:
                print(f"All items downloaded: {total_items_downloaded} in total.")
                break

        except googleapiclient.errors.HttpError as error:
            print(f"An error occurred: {error}")
            break

def download_media(url, filename, creation_date):
    """Download a media item given its URL and save it with the specified filename in the date-specific folder."""
    folder_path = f"photos/{creation_date}"
    
    # Ensure the directory for the creation date exists
    os.makedirs(folder_path, exist_ok=True)

    # Create the full path for the file
    filepath = os.path.join(folder_path, filename)

    try:
        # Add "=d" to download the full resolution
        download_url = url + "=d"
        print(f"Downloading {filename} from {download_url}")
        response = requests.get(download_url)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {filepath}")
        else:
            print(f"Failed to download {filename}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

if __name__ == '__main__':
    # Authenticate and create the service
    service = authenticate_google_photos()
    
    # List and download all photos and videos, handling pagination
    list_photos_and_videos(service)
