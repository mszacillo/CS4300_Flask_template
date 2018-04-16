from . import *
from sim_functions import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

from flask import Flask, request

with open("./app/helper_functions/songData.json", "r") as f:
	song_transcripts = json.load(f)

SONGS = [song_transcripts[index] for index in song_transcripts]
print("loading this page")


@irsystem.route('search',methods=["POST"])
def getQuery():
	inputquery = request.form['search'].lower()
	returnquery = runQuery(inputquery.lower())
	data = []
	for i in returnquery:
		data.append({'title':SONGS[i[1]]['title'],'artist':SONGS[i[1]]['artist'],'score':i[0]})
	return json.dumps({'status':'OK', "data":data})

def runQuery(query):
	tokenized_songs = tokenize_transcript(SONGS)
	n_songs = len(tokenized_songs)
	inv_idx = build_inverted_index(tokenized_songs)
	idf = compute_idf(inv_idx, n_songs)
	doc_norms = computer_doc_norms(inv_idx, idf, n_songs)
	scores = song_search(query.lower(), inv_idx, idf, doc_norms)
	return scores[0:10]
