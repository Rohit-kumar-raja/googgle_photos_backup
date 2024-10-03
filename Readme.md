# Google Photos Downloader

This Python script allows you to authenticate with the Google Photos API and download all your photos and videos, organizing them into folders based on their creation date.

## Features

- Authenticate with Google Photos API using OAuth 2.0.
- List and download all photos and videos from your Google Photos library.
- Organize downloaded files by their creation date.
- Handles pagination to download large photo libraries.

## Prerequisites

To use this script, you need to have:

1. **Google Cloud Project** with the **Google Photos API** enabled.
2. **OAuth 2.0 credentials** file (`credentials.json`) from your Google Cloud project.
3. Python 3.x installed on your system.
4. Required Python libraries installed.

## Setup

### Step 1: Create a Google Cloud Project and Enable Google Photos API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. In the **API & Services** section, enable the **Google Photos Library API**.
4. Create **OAuth 2.0 credentials** (download the `credentials.json` file).
5. Save the `credentials.json` file in the same directory as the script.

### Step 2: Install Required Libraries

Install the required Python libraries using the following command:

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

### Step 3: Run the Script

Run the script to start downloading your Google Photos:

```bash
python google_photos_downloader.py
```

The script will:

1. Open a web browser for you to authenticate with your Google account.
2. Download all photos and videos, organizing them into folders by creation date.

### Step 4: Organize Downloads

The downloaded media files will be saved inside the `photos/` folder, with subfolders named by the creation date of the media (e.g., `photos/2024-01-01/`).

## Code Structure

- `authenticate_google_photos()`: Handles authentication with Google Photos API and returns the service object.
- `list_photos_and_videos(service)`: Lists and downloads photos and videos, handling pagination to ensure all items are downloaded.
- `download_media(url, filename, creation_date)`: Downloads each media item and saves it in the appropriate folder.

## Files

- `google_photos_downloader.py`: The main script for downloading Google Photos.
- `credentials.json`: Your OAuth 2.0 credentials from Google Cloud.
- `token.json`: Stores your authentication tokens (generated automatically after the first authentication).

## Error Handling

- If the `token.json` is expired or invalid, the script will automatically refresh the token.
- The script handles HTTP errors and retries downloading if a failure occurs.

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

