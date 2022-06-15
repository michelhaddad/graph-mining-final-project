import string
from spotipy import SpotifyClientCredentials, Spotify
from requests.exceptions import ReadTimeout


def __extract_info_from_artist_entity(artist_entity: dict):
    return {
        'id': artist_entity['id'],
        'name': artist_entity['name'],
        'followers': artist_entity['followers']['total'],
        'genres': artist_entity['genres'],
        'popularity': artist_entity['popularity']
    }


def spotify_client(client_id, client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    return Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=3, retries=2)


def related_artists(spotify_client: Spotify, artist_id: string):
    try:
        rel_artists = list(map(__extract_info_from_artist_entity, spotify_client.artist_related_artists(artist_id)['artists']))
    except ReadTimeout:
        print('Spotify timed out...')
        return []
    return rel_artists


def artist_features(spotify_client: Spotify, artist_id: string):
    try:
        artist = spotify_client.artist(artist_id)
        rel_artists = related_artists(spotify_client, artist_id)
    except ReadTimeout:
        print('Spotify timed out...')
        return {}

    features = __extract_info_from_artist_entity(artist)
    features['related_artists'] = rel_artists

    return features


# if __name__ == 'main':
client_id = '87cb291862554e369237c3a3f841a0d8'
client_secret = '90cd45d4b3dd426cb1db115bb38d3e2d'

hornet_id = '1kwzW1IszUiq4Gs9BFesvW'
sp = spotify_client(client_id, client_secret)
# hornet_la_frappe = artist_features(sp, hornet_id)
print(related_artists(sp, hornet_id))
