import requests, json, sys

def getSongsSpotify(song_name,access_token):
    """Search For the Song"""
    query = "https://api.spotify.com/v1/search?q={}&type=track&limit=20&offset=0".format(song_name)
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    response_json = response.json()
    print("RESPONSE_GETSONGSSPOTIFY : {}".format(response_json))
    songs = response_json["tracks"]["items"]
    if(len(songs)<5):
        uri = [songs[0]["uri"]]
        names = [songs[0]["name"]]
        artists = [songs[0]["artists"][0]["name"]]
        imageUrl = [songs[0]["album"]["images"][-1]["url"]]
        response_obj = {
            "uri" : uri,
            "names" : names,
            "artists" : artists,
            "images" : imageUrl
        }
    else:
        uri = [ songs[i]["uri"] for i in range(0,5)]
        names = [songs[i]["name"] for i in range(0,5)]
        artists = [songs[i]["artists"][0]["name"] for i in range(0,5)]
        imageUrl = [songs[i]["album"]["images"][-1]["url"] for i in range(0,5)]
        response_obj = {
            "uri" : uri,
            "names" : names,
            "artists" : artists,
            "images" : imageUrl
        }
    return response_obj


def create_playlist(access_token):
    """Create A New Playlist"""
    request_body = json.dumps({
        "name": "Youtube Liked Vids",
        "description": "All Liked Youtube Videos",
        "public": True
    })
    userId = "31q3a5mzo7qu53bfj7x6csdewk7a"
    query = "https://api.spotify.com/v1/users/{}/playlists".format(
            userId)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    response_json = response.json()
    print("create_playlist_id : {}".format(response_json),file = sys.stdout)
    return response_json["id"]

def add_song_to_playlist(uri,access_token):
    """Add all liked songs into a new Spotify playlist"""
    # populate dictionary with our liked songs
    # collect all of uri
    
    # create a new playlist
    playlist_id = create_playlist(access_token)
    print("PlayList Id : {}".format(playlist_id),file = sys.stdout)

    # add all songs into new playlist
    payload = {
        "uris" : [uri],
    }

    payload = json.dumps(payload)
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)


    response = requests.post(
            query,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(access_token)
            }
        )
    # check for valid response status
    if response.status_code != 200:
        return { 'response_code' : response.status_code}
    else:
        response_json = response.json()
        return {'response' : response_json }