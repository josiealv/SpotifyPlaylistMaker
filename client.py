import json
import os
import requests
from track import Track
from playlist import Playlist

name = "name"
id_str = "id"
artists = "artists"
items = "items"
track_str = "track"
tracks_str = "tracks"
url = "external_urls"
spotify = "spotify"
audio_features = "audio_features"
mode_str = "mode"
energy = "energy"
tempo = "tempo"
valence = "valence"
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

    # get recommended tracks based on number of tracks user wants, seeds' average of audio features (instrumentalness, energy, tempo, valence),
    # & whether these seeds are primarily in Major or Minor key (mode)
    def get_recommendations_audio_features (self, json_response, total_seeds, seeds_url, limit):
        instrumentalness = 0
        mode = 0
        energy_avg = 0
        tempo_avg = 0
        valence_avg = 0
        mode1 = 0
        mode0 = 0
        for audio in json_response[audio_features]:
            if(audio[mode_str]==1):
                mode1+=1
            else:
                mode0+=1
            energy_avg += audio[energy] 
            tempo_avg += audio[tempo]
            valence_avg += audio[valence]
        mode = max(mode1, mode0) # check if the seed tracks are mainly in Major or Minor key
        energy_avg /= total_seeds # calculate averages
        tempo_avg /= total_seeds
        valence_avg /= total_seeds
        
        endpoint_seeds = f"https://api.spotify.com/v1/recommendations?seed_tracks={seeds_url}&target_mode={mode}&target_energy={energy_avg}&target_tempo={tempo_avg}&target_valence={valence_avg}&limit={limit}"
        response = self.get_api_request(endpoint_seeds) # get recommended tracks
        return response.json() # return json response 

    # get most recently played tracks, number of tracks based on user input for limit
    def get_last_played_tracks(self, limit=15):
        endpoint = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}" 
        response = self.get_api_request(endpoint)
        json_response = response.json()
        tracks = [Track(track[track_str][name], track[track_str][artists][0][name], track[track_str][id_str]) for
                  track in json_response[items]] # build list of Track objects from json response
        return tracks

    # get track recommendations based on seeds and seeds' audio features to create a more cohesive playlist
    def get_recommedations(self, seeds, limit=15): 
        seeds_url = ""
        for seed in seeds:
            seeds_url += seed.id + "," 
        endpoint_audio_features = f"https://api.spotify.com/v1/audio-features?seed_tracks={seeds_url}"
        response = self.get_api_request(endpoint_audio_features) # get the audio features of the seed tracks
        json_response = self.get_recommendations_audio_features(response.json(), len(seeds), seeds_url, limit) # get the track recommendations based on said audio features
        recommendations = [Track(track[name], track[artists][0][name], track[id_str]) for
                  track in json_response[tracks_str]] # build list of Track objects from json response
        return recommendations

    # create playlist and use recommended tracks to populate the playlist
    def create_playlist (self, name, playlist_tracks):
        data_playlist = json.dumps({
            "name": name,
            "description": "bangerz",
            "public": True
        })
        endpoint_playlist = f"https://api.spotify.com/v1/users/{self.user_id}/playlists" 
        response = self.post_api_request(endpoint_playlist, data_playlist) # create playlist
        json_response = response.json() 
        playlist = Playlist(name, json_response[id_str], json_response[url][spotify]) # use json response to create Playlist object

        track_uris = [track.create_spotify_uri() for track in playlist_tracks] # array for recommended track uri's 
        data_add_tracks = json.dumps(track_uris) 
        endpoint_add_tracks = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks" # populate playlist
        response = self.post_api_request(endpoint_add_tracks, data_add_tracks)
        return playlist
