# Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of applications following the 12-factor principles.

from dotenv import load_dotenv
import os
import base64
from requests import post,get
# Requests allows you to send HTTP/1.1 requests extremely easily
import json
import numpy as np
import pandas as pd

indian_singers = pd.read_csv('indian_singers.csv')
# Environment variables: The os module enables you to access and modify environment variables within your Python program. You can retrieve the value of an environment variable, set a new value, or manipulate the environment as a whole.

load_dotenv() # take environment variables from .env.

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# print(client_id, client_secret)
# https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow

# grant_type	Required Set it to client_credentials.
def get_token():
    auth_string = client_id+":"+client_secret
# encoding this string in utf-8
# Python String encode() converts a string value into a collection of bytes, using an encoding scheme specified by the user
    auth_bytes = auth_string.encode("utf-8")
# Encoding with base64
# Optional altchars must be a bytes-like object of length 2 which specifies an alternative alphabet for the + and / characters
    auth_base64 =str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization":"Basic  "+auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type":"client_credentials"}
    # returns a response object
    result_token = post(url,headers=headers,data=data)
    # response.content returns the content of the response, in bytes. Basically, it refers to Binary Response content.
    #  In Python, JSON data is usually represented as a string.
    # The loads() method is used to parse JSON strings in Python and the result will be a Python dictionary.
    json_result_token= json.loads(result_token.content)
    
    token = json_result_token["access_token"]
    return token


# print(token) #Getting our authorization token
'''Base64 encoding:
It is a type of conversion of bytes to ASCII characters. the list of available Base64 characters are mentioned below:

26 uppercase letters
26 lowercase letters
10 numbers
+ and / for new lines
'''
# For future request
def get_auth_header(token):
    return {"Authorization":"Bearer "+token}
# Look Json documents in order to understand how to access required information or values
for i in indian_singers['singers'] :
    def search_for_artist(token,artist_name):
    # Taken endpoint form spotify documentaion
       url = "https://api.spotify.com/v1/search"
       headers = get_auth_header(token)
    #  F-strings provide a concise and convenient way to embed python expressions inside string literals for formatting. 
       query = f"?q={artist_name}&type=artist&limit=5"
       query_url = url+query
       result_artist = get(query_url,headers=headers)
    # json_result = json.loads(result.content)
       json_result_artist = json.loads(result_artist.content)['artists']['items']
       if len(json_result_artist)==0:
         print('no artist found')
         return None 
       return json_result_artist[0] #returning first artist name
    # print(json_result)

    def get_songs_by_artist(token,artist_id):
      url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=IN"
      headers = get_auth_header(token)
      result_tracks = get(url,headers=headers)
      json_result_tracks = json.loads(result_tracks.content)['tracks']
      return json_result_tracks

    token = get_token()
    artist_names = search_for_artist(token,i)
# print(artist_names)
    artist_name=artist_names['name']
    artist_id = artist_names['id']
    songs = get_songs_by_artist(token,artist_id)
# print(songs)

# Enumerate() method adds a counter to an iterable and returns it in a form of enumerating object. 
    for idx,song in enumerate(songs):
    #    print(f"{idx+1}.{song['name']}")
         if idx ==0:
            top_tracks = artist_name+","+f"{idx+1}.{song['name']}"+","
         elif idx==9:
            top_tracks = f"{idx+1}.{song['name']}"+"\n"
         else:
             top_tracks = f"{idx+1}.{song['name']}"+","
         with open("top_tracks_part.csv", "a") as o:
            o.write(top_tracks)
         










