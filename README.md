# YouTube Trending to Spotify Playlist

This Python script scrapes YouTube's trending videos and adds the songs to a specified Spotify playlist.

## Requirements

- Python 3.6+
- Install the dependencies:
  pip install beautifulsoup4 selenium spotipy

## Setup
- Spotify Developer Credentials: Create an app in Spotify Developer Dashboard to get your client_id and client_secret.
- Modify the Script: Replace the placeholders for client_id and client_secret in the script.
- Playlist: The script assumes you have a playlist named "test-yt". If not, create it or modify the script to use a different playlist name.

## Usage
- Run the script: python your_script.py
- Choose the country code (e.g., us, ro).
   
## The script will:

- Scrape trending YouTube videos.
- Search for them on Spotify.
- Add the found songs to your "test-yt" playlist
