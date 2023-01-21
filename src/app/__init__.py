from flask import Flask, request, url_for, redirect, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
app_obj = Flask(__name__)
app_obj.config.from_object(Config)
db = SQLAlchemy(app_obj)

migration = Migrate(app_obj, db)

TOKEN_INFO = "TOKEN_INFO"

def create_spotify_oauth():
    return SpotifyOAuth(
       client_id = "95fb0bcc0a394d2dad907038cf89c85c",
       client_secret = "bca598d050a04ed98210600f58cddff0",
       redirect_uri= url_for("redirectSite", _external = True),
       scope="user-library-read")
    

@app_obj.route("/")

def start():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app_obj.route("/redirect")

def redirectSite():
  sp_oauth = create_spotify_oauth()
  session.clear()
  code = request.args.get('code')
  token_info = sp_oauth.get_access_token(code)
  session[TOKEN_INFO] = token_info
  return redirect(url_for("getTopArtists", _external = True))


def get_token():

    token = session.get(TOKEN_INFO, None)

    if not token:
        raise "exception"
    
    now = int(time.time())

    expired = token['expires_at'] - now < 60
    
    if(expired):
        sp_auth = create_spotify_oauth()
        token = sp_auth.refresh_access_token(token['refresh_token'])
    return token



@app_obj.route("/topArtists", methods= ["GET", "POST"])

def getTopArtists():


        try:
            token = get_token()
        except:
            print("the user is not logged in")
            redirect("/")
    
    
        sp = spotipy.Spotify(auth =token['access_token'])
        return sp.current_user_top_tracks(limit = 10, offset = 0, time_range = "medium_term")

    
