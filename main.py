from client import Client

def main():
    user_id = input("Please enter user id/username (NOTE: this is different from your display name, this can be found in account ovierview)\n")
    print ("Go to this site: https://developer.spotify.com/console/post-playlists/ \n")
    print ("Enter user_id in empty 'user_id' text box & click 'Get Token' button \n")
    print ("Select the following:\n")
    print ("playlist-modify-public\n")
    print ("playlist-modify-private\n")
#  print ("Select the following:\n")
    auth_token = input ("Enter genereated OAuth Token:\n")
    cli = Client(auth_token, user_id)