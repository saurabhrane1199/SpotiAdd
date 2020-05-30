from flask import Flask, jsonify, request
import os, requests, sys, json
import google_auth_oauthlib.flow, googleapiclient.discovery, googleapiclient.errors
import secret, spotifyHelper


scopes = ["https://www.googleapis.com/auth/youtube"]

app = Flask(__name__)

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
    return response


@app.route('/<vid>', methods = ['GET'])
def getvideoTitle(vid):
    access_token = request.args.get('code')
    print("access_code : {}".format(access_token),file = sys.stdout)
    response = getResponseYTAPI(vid)
    data = response["items"][0]['snippet']
    title = data['title'].split('-')[0]
    print("Title : {}".format(title),file = sys.stdout)
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
        print("URI : {}".format(uri),file = sys.stdout)
        # response = add_song_to_playlist(uri,access_token)
        # print("FIN_RESPOnSE ; {}".format(response),file = sys.stdout)
        return jsonify(uri)
       

if __name__ == '__main__':
    app.run(debug=True)   