#using python 2.7

import requests
from musixmatch import Musixmatch
import json

apiKey = "14c95a1eab8c1db9d79d0e06f0d3cc1d"

musixmatch = Musixmatch(apiKey)

def gettop100():
	lyrics_json = {}
	top100 = musixmatch.chart_tracks_get(1, 100,f_has_lyrics=1)
	for song in top100['message']['body']['track_list']:
		song = song['track']
		track_id = song['track_id']
		track_name = song['track_name']
		artist_name = song['artist_name']
		artist_id = song['artist_id']
		track_rating = song['track_rating']
		track_length = song['track_length']
		lyrics = musixmatch.track_lyrics_get(track_id)['message']['body']['lyrics']['lyrics_body']
		lyrics_json[track_id] = {'track_id':track_id, 'track_name': track_name, 'track_rating':track_rating,'lyrics':lyrics
		,'track_length':track_length, 'artist_name':artist_name, 'artist_id':artist_id}
	return lyrics_json

def savejson(data):
	with open('data.json', 'w') as outfile:
		json.dump(data, outfile)

top100 = gettop100()
savejson(top100)

