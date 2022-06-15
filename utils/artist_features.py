import string
from spotipy import SpotifyClientCredentials, Spotify


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
    return Spotify(client_credentials_manager=client_credentials_manager)


def related_artists(spotify_client: Spotify, artist_id: string):
    return list(map(__extract_info_from_artist_entity, spotify_client.artist_related_artists(artist_id)['artists']))


def artist_features(spotify_client: Spotify, artist_id: string):
    artist = spotify_client.artist(artist_id)
    rel_artists = related_artists(spotify_client, artist_id)

    features = __extract_info_from_artist_entity(artist)
    features['related_artists'] = rel_artists

    return features


# if __name__ == 'main':
client_id = '7641b1dcfa894b9e97d9419d50e29c45'
client_secret = '7641b1dcfa894b9e97d9419d50e29c45'

hornet_id = '1kwzW1IszUiq4Gs9BFesvW'
sp = spotify_client(client_id, client_secret)

hornet_la_frappe = artist_features(sp, hornet_id)
print(related_artists(sp, hornet_id))
