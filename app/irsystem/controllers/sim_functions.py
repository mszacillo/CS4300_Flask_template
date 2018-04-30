import re
import json
import time
import math
import copy
from nltk.tokenize import TreebankWordTokenizer
from difflib import SequenceMatcher

import numpy as np

tokenizer = TreebankWordTokenizer()

def similar(a,b):
	return SequenceMatcher(None, a, b).ratio()

def tokenize_transcript(temp):
	for idx, song in enumerate(temp):
		lyrics = song["lyrics"]
		lyrics = lyrics.replace("\\n", " ").replace("[Hook", " ").replace("[Verse", " ").replace("b", " ", 1)
		temp[idx]["lyrics"] = re.findall(r"[a-z]+", lyrics.lower())

	return temp

def build_inverted_index(songs):
	indexdict = {}

	for i,x in enumerate(songs):
		counter_dict = {}
		for word in x["lyrics"]:
			if word in counter_dict:
				counter_dict[word] +=1
			else:
				counter_dict[word] =1
		for term,freq in counter_dict.items():
			if term not in indexdict:
				indexdict[term] = []
			indexdict[term].append((i,counter_dict[term]))

	return indexdict

def compute_idf(inv_idx, n_songs, min_df=10, max_df_ratio=0.95):
	idf = {}

	for i in inv_idx:
		if((len(inv_idx[i]) < min_df) or (float(len(inv_idx[i]))/n_songs > max_df_ratio)):
			continue
		else:
			#calculate log base 2
			idf[i] = math.log(float(n_songs)/(1 + len(inv_idx[i]))) / math.log(2)

	return idf

def computer_doc_norms(inv_idx, idf, n_songs):

	norms = np.zeros(n_songs)

	for term in idf:
		for doc_id, tf in inv_idx[term]:
			norms[doc_id] += (tf*idf[term])**2

	return np.sqrt(norms)

def song_search(query, index, idf, songs, doc_norms):

	querytokens = tokenizer.tokenize(query)
	uniquetokens = np.unique(querytokens)

	temp = np.zeros(len(doc_norms))
	qnorm = 0
	for word in uniquetokens:
		if word in idf:
			qnorm = qnorm + (idf[word]*querytokens.count(word))**2
		else:
			continue

	for word in uniquetokens:
		if word not in index:
			continue
		else:
			qtf = querytokens.count(word)
			for doc, tf in index[word]:
				if word in idf:
					temp[doc] = temp[doc] + ((tf * qtf)*(idf[word]**2))

	qnorm = math.sqrt(qnorm)
	temp = np.divide(temp, qnorm)

	where_are_NaNs = np.isnan(temp)
	temp[where_are_NaNs] = 0
	
	results = []

	for idx, dnorm in enumerate(doc_norms):
		if(dnorm != 0):
			score = ((temp[idx]/dnorm) * 0.5) + (similar(query.lower(),songs[idx]["title"].lower()) * 0.5)
			results.append((score, idx))
		else:
			score = ((temp[idx] * 0.5) + (similar(query.lower(),songs[idx]["title"].lower()) * 0.5))
			results.append((score, idx))
	
	return sorted(results, key=lambda x: x[0], reverse=True)	

def closest_songs(project_index_in, docs_compressed, k=10):
	sims = docs_compressed.dot(docs_compressed[project_index_in,:])
	asort = np.argsort(-sims)[:k+1]
	results = [(1, project_index_in)] + [(sims[i]/sims[asort[0]], i) for i in asort[1:]]	
	return results

def svd_cosine(scores, closest):
	idx_to_score = {}
	results = []
	for score, idx in scores:
		if idx not in idx_to_score.keys():
			idx_to_score[idx] = score

	for score, idx in closest:
		if idx not in idx_to_score.keys():
			idx_to_score[idx] = score
		else:
			idx_to_score[idx] = idx_to_score[idx] + (score*0.3)

	for idx, score in idx_to_score.items():
		results.append((score, idx))

	return sorted(results, key=lambda x: x[0], reverse=True)	

