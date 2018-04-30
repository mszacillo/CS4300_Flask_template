from . import *
from sim_functions import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize

from flask import Flask, request

with open("./app/helper_functions/songData.json", "r") as f:
	song_transcripts = json.load(f)

print("loading this page")

SONGS = [song_transcripts[index] for index in song_transcripts]
songlist = [song["lyrics"] for song in SONGS]
vectorizer = TfidfVectorizer(stop_words = "english",max_df=.8)
docs_compressed = svds(vectorizer.fit_transform(songlist).transpose(), k = 40)[2].transpose()
tokenize_transcript(SONGS)
inv_idx = build_inverted_index(SONGS)
idf = compute_idf(inv_idx, len(SONGS))
doc_norms = computer_doc_norms(inv_idx, idf, len(SONGS))

@irsystem.route('search',methods=["POST"])
def getQuery():
	#docs_compressed = docs_compressed.transpose()

	my_json = request.get_json()
	inputquery = my_json.get('search').lower()
	returnquery = runQuery(inputquery.lower(), inv_idx, idf, SONGS, doc_norms, docs_compressed)
	data = []
	for score, idx in returnquery:
		#lyrics = " ".join(tokenize_one_transcript(i[1]['lyrics']))
		lyrics = SONGS[idx]["lyrics"]
		lyrics = " ".join(lyrics)
		data.append({'title':SONGS[idx]['title'],'artist':SONGS[idx]['artist'],'score':score,'lyrics':lyrics})
	return json.dumps({'status':'OK', "data":data})

def runQuery(query, inv_idx, idf, SONGS, doc_norms, docs_compressed):
	scores = song_search(query.lower(), inv_idx, idf, SONGS, doc_norms)
	toptitle = scores[0][1] 
	closestsongs = closest_songs(toptitle, docs_compressed)
	finalscores = svd_cosine(scores, closestsongs)

	return finalscores[0:10]

# @irsystem.route('search',methods=["POST"])
# def getQuery():
# 	my_json = request.get_json()
# 	inputquery = my_json.get('search').lower()
# 	positive = int(my_json.get('sentiment'))
# 	returnquery = runQueryML(inputquery.lower())
# 	data = []
# 	for i in returnquery:
# 		lyrics = " ".join(tokenize_one_transcript(i[1]['lyrics']))
# 		sentiment = TextBlob(lyrics)
# 		if positive and sentiment.sentiment.polarity >=0:
# 			data.append({'title':i[1]['title'],'artist':i[1]['artist'],'score':i[0],'lyrics':lyrics})
# 		elif not positive and sentiment.sentiment.polarity <=0 :
# 			data.append({'title':i[1]['title'],'artist':i[1]['artist'],'score':i[0],'lyrics':lyrics})
# 	return json.dumps({'status':'OK', "data":data})

# def runQuery(query):
# 	tokenized_songs = tokenize_transcript(SONGS)
# 	n_songs = len(tokenized_songs)
# 	inv_idx = build_inverted_index(tokenized_songs)
# 	idf = compute_idf(inv_idx, n_songs)
# 	doc_norms = computer_doc_norms(inv_idx, idf, n_songs)
# 	scores = song_search(query.lower(), inv_idx, idf, doc_norms)
# 	return scores[0:10]

# def runQueryML(query):
# 	vectorizer = TfidfVectorizer(stop_words = "english",max_df=.8)
# 	songlist = [song["lyrics"] for song in SONGS]
# 	songlist.append(query)
# 	lyric_matrix = vectorizer.fit_transform(songlist).transpose()
# 	#print(lyric_matrix.shape)
# 	#u, s, v = svds(lyric_matrix, k=100)
# 	words_compressed, _, docs_compressed = svds(lyric_matrix, k = 40)
# 	docs_compressed = docs_compressed.transpose()

# 	word_to_index = vectorizer.vocabulary_

# 	index_to_word = {i:t for t,i, in word_to_index.items()}
# 	words_compressed = normalize(words_compressed, axis =1)

# 	docs_compressed = normalize(docs_compressed, axis=1)
# 	return closest_songs(docs_compressed.shape[0]-1,docs_compressed)


# def closest_songs(project_index_in,docs_compressed, k=50):
# 	sims = docs_compressed.dot(docs_compressed[project_index_in,:])
# 	asort = np.argsort(-sims)[:k+1]
# 	print(len(asort))
# 	return [(sims[i]/sims[asort[0]],SONGS[i]) for i in asort[1:]]
