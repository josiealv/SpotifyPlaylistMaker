import json
import os
import requests
from track import Track
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

name = "name"
id_str = "id"
artists = "artists"
tracks = "tracks"
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
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response
    def get_last_played_tracks(self, limit=15):
        endpoint = "https://api.spotify.com/v1/me/player/recently-played?limit={limit}" 
        response = self.get_api_request(endpoint)
        json_response = response.json()
        tracks = [Track(track[name], track[artists][0][name], track[id_str]) for
                  track in json_response[tracks]] # tracks might be items instead
