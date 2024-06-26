from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def fetch_billboard_songs(date):
    url = f"https://www.billboard.com/charts/hot-100/{date}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        song_names_spans = soup.select("li span.chart-element__information__song")
        song_names = [song.getText().strip() for song in song_names_spans]
        return song_names
    else:
        print(f"Failed to fetch Billboard Hot 100 for {date}. Status code: {response.status_code}")
        return []

def search_spotify_for_songs(sp, song_names, year):
    song_uris = []
    for song in song_names:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    return song_uris

def create_spotify_playlist(sp, user_id, date, song_uris):
    playlist_name = f"{date} Billboard 100"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    print(f"Playlist '{playlist_name}' created successfully.")
    return playlist

def main():
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

    song_names = fetch_billboard_songs(date)
    if not song_names:
        return
    
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://example.com",
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
            show_dialog=True,
            cache_path="token.txt"
        )
    )
    user_id = sp.current_user()["id"]
    print(f"Logged in as {user_id}")

    year = date.split("-")[0]
    song_uris = search_spotify_for_songs(sp, song_names, year)

    if song_uris:
        create_spotify_playlist(sp, user_id, date, song_uris)

if __name__ == "__main__":
    main()
