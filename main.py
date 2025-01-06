from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

def remove_emojis(text):
    if isinstance(text, str):  # Ensure input is a string
        emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)  # Emojis Unicode range
        return emoji_pattern.sub(r'', text)
    return text

#get youtube trending:
options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
country = input("Pick the country (2 letters): ").lower()
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url = f"https://charts.youtube.com/charts/TrendingVideos/{country}/RightNow"
driver.get(url)
time.sleep(5)
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
driver.quit()

artist_elements = soup.find_all('span', class_='style-scope ytmc-entry-row', hidden=True)
song_elements = soup.find_all('div', class_='title style-scope ytmc-entry-row')

#spotify login
client_id = 'aaa'
client_secret = 'bbb'
scope = 'playlist-modify-public playlist-modify-private user-library-read'
redirect_uri = 'http://localhost:8888/callback'

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#sp = spotipy.Spotify(auth_manager=auth_manager)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope))

playlists = sp.current_user_playlists()
playlist_id = None
for playlist in playlists['items']:
    if playlist['name'] == 'test-yt':
        playlist_id = playlist['id']
        break

if not playlist_id:
    print('Playlist "test-yt" not found.')
else:
    for artist, song in zip(artist_elements, song_elements):
        artist_name = remove_emojis(artist.get_text(strip=True))
        song_title = remove_emojis(song.get_text(strip=True))
        print(f"Artist: {artist_name}, Song: {song_title}")
        print(f"search for {artist_name} - {song_title}")
        search_query = f'{song_title} {artist_name}'
        results = sp.search(q=search_query, limit=1, type='track')
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_uri = track['uri']

            sp.playlist_add_items(playlist_id, [track_uri])
            print(f'Successfully added "{song_title}" by {artist_name} to the "test-yt" playlist.')
        else:
            print(f'Song "{song_title}" by {artist_name} not found on Spotify.')
        print('------------')
