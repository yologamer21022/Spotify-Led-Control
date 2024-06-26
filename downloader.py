from spotipy.oauth2 import SpotifyOAuth

import requests
import os

# Set up the Spotify OAuth parameters
scope = "user-library-read"  # Set the desired scope
username = "None"  # Replace with your Spotify username
client_id = "None"  # Replace with your Spotify client ID
client_secret = "None"  # Replace with your Spotify client secret
redirect_uri = "None"  # Replace with your redirect URI


def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image.")



def delete_cache(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Failed to delete {filepath}: {e}")


def main(song):
    delete_cache("cache")
    query = song


    # Create the SpotifyOAuth object
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

    # Get the access token
    access_token = sp_oauth.get_access_token(as_dict=False)
    if access_token:
        print(access_token)
    else:
        print("Unable to retrieve access token.")

    # Make the GET request to the Spotify Web API
    response = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": query, "type": "track", "limit": 1},
        headers={"Authorization": "Bearer " + access_token}
    )

    # Extract the image URL from the response
    data = response.json()
    if "tracks" in data and "items" in data["tracks"] and len(data["tracks"]["items"]) > 0:
        image_url = data["tracks"]["items"][0]["album"]["images"][0]["url"]
        # Specify the folder and file name
        folder = "cache"
        file_name = "album_image.jpg"
        
        # Create the folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Construct the file path
        file_path = os.path.join(folder, file_name)

        # Download the image
        download_image(image_url, file_path)



