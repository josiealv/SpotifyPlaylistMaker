class Track:
    def __init__(self, name, artist, id):
        self.name = name
        self.id = id
        self.artist = artist
    def create_spotify_uri(self):  # creates string of the track's uri
        return f"spotify:track:{self.id}"
