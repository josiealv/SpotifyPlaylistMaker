from client import Client

def main():
    user_id = input("Please enter user id/username (NOTE: this is different from your display name, this can be found in account ovierview)\n")
    print ("Go to this site: https://developer.spotify.com/console/post-playlists/ \n")
    print ("Enter user_id in empty 'user_id' text box & click 'Get Token' button \n")
    print ("Select the following:\n")
    print ("playlist-modify-public\n")
    print ("playlist-modify-private\n")
    print ("user-read-recently-played:\n")
    auth_token = input ("Enter genereated OAuth Token:\n")
    cli = Client(auth_token, user_id)

    num_tracks = int(input("How many of your recently played tracks would you like to see? "))
    last_tracks = cli.get_last_played_tracks(num_tracks)

    print("Here are your last "+ str(num_tracks) + " played")
    for i, track in enumerate(last_tracks):
        print(f"{i+1}. {track.name} by {track.artist}")

main()