from bs4 import BeautifulSoup
import requests
import password
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? type the hate in this format YYYY-MM-DD")

# date = "2023-07-14"

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")

soup = BeautifulSoup(response.text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

song_artists_spans = soup.select("li ul li span")
song_artists = [song.getText().strip() for song in song_artists_spans if len(song.getText().strip()) > 2]

print(song_names)
print(song_artists)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=password.clientID,
        client_secret=password.ClientSecret,
        show_dialog=True,
        cache_path="token.txt",
        username="matteo.genovese-it",
    )
)
user_id = sp.current_user()["id"]

# Creazione della playlist
playlist_name = f"BillboardHot100-{date}"
playlist_description = "Done with my app"
playlist = sp.user_playlist_create(user_id, playlist_name, public=False, collaborative=False,
                                   description=playlist_description)
playlist_id = playlist["id"]

# Aggiunta della traccia alla playlist
year = date.split("-")[0]

for song in song_names:
    song_response = sp.search(q='track:' + song + " year:" + year, type='track')
    try:
        uri = song_response["tracks"]["items"][0]["uri"]
        sp.playlist_add_items(playlist_id, [uri])
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")