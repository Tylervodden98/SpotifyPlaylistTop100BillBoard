import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pprint

YEAR_SEARCH = 2012
#FOR FETCHING 100 SONG LIST
#yearoftravel 2012-10-22
year_of_travel = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{year_of_travel}")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")
song_list_100 = soup.find_all(class_="a-font-primary-bold-s")
cut_atags_songs = []
print(song_list_100)

for song in song_list_100:
    try:
        if song.name == "h3":
            cut_atags_songs.append(song.text.strip())
    except AttributeError:
        print("Not h3 tag")

cut_atags_songs.pop(0)
cut_atags_songs.pop(0)

#Spotify Setup
load_dotenv(r"../SpotifyPlaylistfromTop100/toks.env")
# FOR SPOTIFY API
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

#Authenticate spotipy
print(CLIENT_ID)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope='playlist-modify-private'))
spotify_user_name = sp.current_user()['id']
print(spotify_user_name)

song_uri = []
#Search spotipy
for songs in cut_atags_songs:
    try:
        result = sp.search(q=f"track:{songs} year:{YEAR_SEARCH}",limit=1)
        each_song_uri = result["tracks"]["items"][0]['uri']
        print(each_song_uri)
        song_uri.append(each_song_uri)
    except IndexError:
        print(f"{songs} doesn't exist in Spotify, skipped.")

#Making Private playlist
playlist_name = sp.user_playlist_create(user=spotify_user_name,name=f" Billboard 100", public=False)
playlist_id = playlist_name['id']
sp.playlist_add_items(playlist_id=playlist_id,items=song_uri)
print(playlist_name)
print(playlist_id)
print(song_uri)


