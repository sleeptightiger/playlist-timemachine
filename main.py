from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth



scope = "playlist-modify-private"

CLIENT_ID = ""
CLIENT_SECRET = ""
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)






url_endpoint = "https://www.billboard.com/charts/hot-100/"
# date = input("Enter a date you would like to time travel back to(YYYY-MM-DD)... ")
date = "1990-06-11"

response = requests.get(url_endpoint + date)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
song_titles_list = []
artists_list = []
song_names = []
song_titles = soup.find_all("h3", id="title-of-a-story", class_="a-no-trucate")
artists = soup.find_all("span", class_="a-no-trucate")
for song in song_titles:
    song_titles_list.append(song.string.strip())

for artist in artists:
    artists_list.append(artist.string.strip())

for i in range(0, len(song_titles_list)):
    song_names.append(song_titles_list[i] + " - " + artists_list[i])

user_id = sp.current_user()["id"]
# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)