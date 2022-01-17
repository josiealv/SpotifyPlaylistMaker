from client import Client

def main():
    user_id = input("Please enter user id/username (NOTE: this is different from your display name, this can be found in account ovierview)\n")
    print("\n")
    print ("Go to this site: https://developer.spotify.com/console/post-playlists/ ")
    print ("Enter user_id in empty 'user_id' text box & click 'Get Token' button ")
    print ("Select the following:")
    print ("playlist-modify-public")
    print ("playlist-modify-private")
    print ("user-read-recently-played")
    auth_token = input ("Enter genereated OAuth Token: \n")
    cli = Client(auth_token, user_id) 
    print("\n")

    num_tracks = int(input("How many of your recently played tracks would you like to see? (Min: 10, Max: 50) "))
    last_tracks = cli.get_last_played_tracks(num_tracks) 
    print("\n")

    print(f"Here are your last {num_tracks} played:")
    for i, track in enumerate(last_tracks):
        print(f"{i+1}. {track.name} by {track.artist}")
    print("\n")

    indexes = input(f"Enter the number of the tracks, separated by a comma, that you want to base the playlist around (Min: 1, Max: {num_tracks}) ")
    indexes = indexes.split(",") 
    seeds = [last_tracks[int (i)-1] for i in indexes]
    num_recs = int (input ("How many recommended tracks would you like (tracks entered earlier will be included in playlist)? (Min: 1, Max: 100) "))
    recommnded_tracks = cli.get_recommedations(seeds, num_recs)
    print("\n")

    recommnded_tracks += seeds # add seed tracks to list so they can be apart of the playlist 
    playlist_name = input("Enter the name of your playlist: ")
    playlist = cli.create_playlist(playlist_name, recommnded_tracks)
    print(f"Created {playlist.name} with recommendded tracks successfully!")
    print(f"url: {playlist.url}") # print link to playlist so user can access it immediately 
main()