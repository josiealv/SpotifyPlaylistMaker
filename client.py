import json
import os
import requests
from track import Track
from playlist import Playlist
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

name = "name"
id_str = "id"
artists = "artists"
items = "items"
track_str = "track"
tracks_str = "tracks"
url = "external_urls"
spotify = "spotify"
class Client:
    def __init__(self, auth_token, user_id):
        self.user_id = user_id
        self.auth_token = auth_token

    def get_api_request(self, endpoint):
        response = requests.get(
            endpoint,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}"
            }
        )
        return response
    def post_api_request(self, endpoint, data):
        response = requests.post(
            endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}"
            }
        )
        return response
    def get_last_played_tracks(self, limit=15):
        endpoint = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}" 
        response = self.get_api_request(endpoint)
        json_response = response.json()
        tracks = [Track(track[track_str][name], track[track_str][artists][0][name], track[track_str][id_str]) for
                  track in json_response[items]] # tracks might be items instead
        return tracks

    def get_recommedations(self, seeds, limit=15):
        seeds_url = ""
        for seed in seeds:
            seeds_url += seed.id + ","
        endpoint = f"https://api.spotify.com/v1/recommendations?seed_tracks={seeds_url}&limit={limit}"
        response = self.get_api_request(endpoint)
        json_response = response.json()
        recommendations = [Track(track[name], track[artists][0][name], track[id_str]) for
                  track in json_response[tracks_str]]
        return recommendations

    def create_playlist (self, name, playlist_tracks):
        data_playlist = json.dumps({
            "name": name,
            "description": "bangerz",
            "public": True
        })
        endpoint_playlist = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self.post_api_request(endpoint_playlist, data_playlist)
        json_response = response.json()
        playlist = Playlist(name, json_response[id_str], json_response[url][spotify])

        track_uris = [track.create_spotify_uri() for track in playlist_tracks]
        data_add_tracks = json.dumps(track_uris)
        endpoint_add_tracks = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self.post_api_request(endpoint_add_tracks, data_add_tracks)
        return playlist
