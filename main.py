from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re

def remove_emojis(text):
    # Emoji pattern (matches most common emojis)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

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

for artist, song in zip(artist_elements, song_elements):
    artist_name = remove_emojis(artist.get_text(strip=True))
    song_title = remove_emojis(song.get_text(strip=True))
    print(f"Artist: {artist_name}, Song: {song_title}")
