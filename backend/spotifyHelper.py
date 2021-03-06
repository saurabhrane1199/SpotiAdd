import requests, json, sys

def getUserId(access_token):
    query = "https://api.spotify.com/v1/me"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    response_json = response.json()
    userId = response_json["id"]
    return userId



def getSongsSpotify(song_name,access_token):
    """Search For the Song"""
    song_name = song_name.strip()
    query = "https://api.spotify.com/v1/search?q={}&type=track&limit=20&offset=0".format(song_name)
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    response_json = response.json()
    # 
    
    songs_no = response_json["tracks"]["total"]
    if songs_no == 0 :
        return {"songs_no" : songs_no}
    songs = response_json["tracks"]["items"]
    if(len(songs)<5):
        uri = [songs[0]["uri"]]
        names = [songs[0]["name"]]
        artists = [songs[0]["artists"][0]["name"]]
        imageUrl = [songs[0]["album"]["images"][-1]["url"]]
        response_obj = {
            "songs_no" : songs_no,
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
            "songs_no" : songs_no,
            "uri" : uri,
            "names" : names,
            "artists" : artists,
            "images" : imageUrl
        }
    return response_obj


def create_playlist(access_token):
    """Create A New Playlist"""
    request_body = json.dumps({
        "name": "SpotiAdd",
        "description": "All Liked Youtube Videos",
        "public": True
    })
    userId = getUserId(access_token)
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
    # print("create_playlist_id : {}".format(response_json),file = sys.stdout)
    return response_json["id"]

def add_song_to_playlist(uri,access_token,playlist_id):
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

def checkIfPlaylistExists(playListname, access_token):
    query = "https://api.spotify.com/v1/me/playlists"
    response = requests.get(
        query,
        headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(access_token)
            }
    )
    if response.status_code != 200:
        return { 'response_code' : response.status_code}
    res = response.json()
    playlistNamesDict = { res['items'][i]["name"] : res['items'][i]["id"]  for i in range(0,len(res['items'])) }
    if playListname in playlistNamesDict.keys():
        playListId = playlistNamesDict[playListname]
        return {
            'playListExists' : True,
            'id' : playListId
        }
    else:
        return {
            'playListExists' : False,
            'id' : None
            }

def artist_equals_query(title, songsObj):
    artist_name = songsObj["artists"][0].lower()
    if title.lower() == artist_name:
        return True
    else:
        return False
    