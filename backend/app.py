from flask import Flask, jsonify, request
import os, requests, sys, json, base64, re
import google_auth_oauthlib.flow, googleapiclient.discovery, googleapiclient.errors
import secret, spotifyHelper, regex

scopes = ["https://www.googleapis.com/auth/youtube"]

app = Flask(__name__)


def encodeStringBase64():
    message = "{}:{}".format(secret.client_id,secret.client_secret)
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def getResponseYTAPI(vid):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = secret.DEVELOPER_KEY
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=vid
    )
    response = request.execute()
    # print("YT Response : {}".format(response),file = sys.stdout)
    return response



@app.route('/oauth', methods=['GET'])
def getOauthCode():
    code = request.args.get('code')
    redirect_uri = request.args.get('ru')
    rf = request.args.get('rf')
    encodedString = encodeStringBase64()
    url = "https://accounts.spotify.com/api/token"
    if(rf == "0"):
        payload = 'grant_type=authorization_code&code={}&redirect_uri={}'.format(code,redirect_uri)
    else:
        payload = 'grant_type=refresh_token&refresh_token={}'.format(code)
    headers = {
        'Authorization': 'Basic {}'.format(encodedString),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(
                    url,
                    headers=headers,
                    data = payload
                    )
    if response.status_code != 200:
        return jsonify({ 'response_code' : response.status_code})
    response_json = response.json()
    # print("response : {}".format(response_json),file = sys.stdout)
    oauth = response_json["access_token"]
    if "refresh_token" in response_json.keys():
        refresh_token = response_json["refresh_token"]
    else:
        refresh_token = "not_defined"
    return jsonify({'oauth' : oauth,
                    'refresh_token' : refresh_token,
                        })




@app.route('/addSong',methods = ['GET'])
def addSongToPlaylist():
    songURI = request.args.get('songUri')
    code = request.args.get('code')
    # print("SONG_URI : {}".format(songURI),file = sys.stdout)
    playListName = "SpotiAdd"
    access_token = code
    response = spotifyHelper.checkIfPlaylistExists(playListName,code)
    if(response["playListExists"]):
        playlistId = response["id"] 
    else:
        playlistId = spotifyHelper.create_playlist(access_token)
    response = spotifyHelper.add_song_to_playlist(songURI,access_token,playlistId)
    return jsonify(response)    



@app.route('/getSongs',methods = ['GET'])
def getSongs():
    title_id = request.args.get('title_id')





@app.route('/<vid>', methods = ['GET'])
def getvideoTitle(vid):
    access_token = request.args.get('code')
    # print("access_code : {}".format(access_token),file = sys.stdout)
    response = getResponseYTAPI(vid)
    data = response["items"][0]['snippet']
    title = regex.getTitles(data["title"])
    # print("Title : {}".format(title),file = sys.stdout)
    category = data['categoryId']
    isMusic = False
    isMusic = category == '10'
    if(not isMusic):
        api_response = {
            'response' : 'not_music' 
        }
        return jsonify(api_response)
    else:
        uri = spotifyHelper.getSongsSpotify(title[0].strip(),access_token)
        if uri["songs_no"] == 0 and len(title)>1:
            new_title = title[0].strip() + " " + title[1].strip()
            # print("New Title Songs: {}".format(new_title),file = sys.stdout)
            uri = spotifyHelper.getSongsSpotify(new_title,access_token)
            return (jsonify({ "response" : "song_not_found"}) if uri["songs_no"] == 0 else jsonify(uri))

        elif uri["songs_no"] == 0 and len(title)==1:
            return jsonify({ "response" : "song_not_found"})
           

        elif spotifyHelper.artist_equals_query(title[0].strip(),uri):
            new_title = title[0].strip() + " " + title[1].strip()
            # print("New Title: {}".format(new_title),file = sys.stdout)
            uri = spotifyHelper.getSongsSpotify(new_title,access_token)
            return (jsonify({ "response" : "song_not_found"}) if uri["songs_no"] == 0 else jsonify(uri))

        else:
            return jsonify(uri)
       

if __name__ == '__main__':
    app.run(debug=True)   