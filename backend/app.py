from flask import Flask, jsonify, request
import os, requests, sys, json, base64
import google_auth_oauthlib.flow, googleapiclient.discovery, googleapiclient.errors
import secret, spotifyHelper

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
    DEVELOPER_KEY = "AIzaSyC0TUermEDZAcRRMPYEwsMpFu3jK8KdxDI"
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
    encodedString = encodeStringBase64()
    url = "https://accounts.spotify.com/api/token"
    payload = 'grant_type=authorization_code&code={}&redirect_uri={}'.format(code,redirect_uri)
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
        return { 'response_code' : response.status_code}
    response_json = response.json()
    oauth = response_json["access_token"]
    return {'oauth' : oauth}




@app.route('/addSong',methods = ['GET'])
def addSongToPlaylist():
    songURI = request.args.get('songUri')
    code = request.args.get('code')
    print("SONG_URI : {}".format(songURI),file = sys.stdout)
    playListName = "SpotiAdd"
    access_token = code
    response = spotifyHelper.checkIfPlaylistExists(playListName,code)
    if(response["playListExists"]):
        playlistId = response["id"] 
    else:
        playlistId = spotifyHelper.create_playlist(access_token)
    response = spotifyHelper.add_song_to_playlist(songURI,access_token,playlistId)
    return jsonify(response)    





@app.route('/<vid>', methods = ['GET'])
def getvideoTitle(vid):
    access_token = request.args.get('code')
    # print("access_code : {}".format(access_token),file = sys.stdout)
    response = getResponseYTAPI(vid)
    data = response["items"][0]['snippet']
    title = data['title'].split('-')[0]
    # print("Title : {}".format(title),file = sys.stdout)
    title.strip()
    category = data['categoryId']
    isMusic = False
    isMusic = category == '10'
    if(not isMusic):
        api_response = {
            'response' : 'not_music' 
        }
        return jsonify(api_response)
    else:
        uri = spotifyHelper.getSongsSpotify(title,access_token)
        # print("URI : {}".format(uri),file = sys.stdout)
        return jsonify(uri)
       

if __name__ == '__main__':
    app.run(debug=True)   