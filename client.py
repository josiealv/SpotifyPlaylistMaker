import json
import os
import requests

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

class Client:
    def __init__(self, auth_token, user_id):
        self.user_id = user_id
        self.auth_token = auth_token


