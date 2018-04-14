from Similarity import *

with open("songData.json", "r") as f:
	song_transcripts = json.load(f)

SONGS = [song_transcripts[index] for index in song_transcripts]

@app.route('/searchQuery')
def getQuery():
	inputquery = request.form['search'];
	returnquery = runQuery(inputquery)
	score = returnquery[0][0]
	idx = returnquery[0][1]
	return json.dumps({'status':'OK', "title": SONGS[idx]['title'], "score": score})

def runQuery():
	query = getQuery()
	tokenized_songs = tokenize_transcript(SONGS)
	n_songs = len(tokenized_songs)
	inv_idx = build_inverted_index(tokenized_songs)
	idf = compute_idf(inv_idx, n_songs)
	doc_norms = computer_doc_norms(inv_idx, idf, n_songs)
	scores = song_search("I love you", inv_idx, idf, doc_norms)
	return scores[0:10]

