import os

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTH_REQUEST = "https://accounts.spotify.com/authorize?client_id=" + CLIENT_ID +"&response_type=code&redirect_uri="