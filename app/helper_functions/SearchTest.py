from sim_functions import *

with open("songData.json", "r") as f:
	song_transcripts = json.load(f)

songs = [song_transcripts[index] for index in song_transcripts]
print(songs[0])
start_time = time.time()
tokenized_songs = tokenize_transcript(songs)
execution_time = time.time() - start_time

print("Tokenization took %f seconds." % execution_time)
n_songs = len(tokenized_songs)

start_time = time.time()
inv_idx = build_inverted_index(tokenized_songs)
execution_time = time.time() - start_time

print("Inverted index took %f seconds." % execution_time)

start_time = time.time()

idf = compute_idf(inv_idx, n_songs)
execution_time = time.time() - start_time

print("IDF took %f seconds." % execution_time)

start_time = time.time()
doc_norms = computer_doc_norms(inv_idx, idf, n_songs)
execution_time = time.time() - start_time

print("Norm took %f seconds." % execution_time)

start_time = time.time()
scores = song_search("I had a good dinner", inv_idx, idf, doc_norms)
execution_time = time.time() - start_time

print("Song search took %f seconds." % execution_time)

for score, idx in scores[0:10]:
	print("%s with a score of %f" % (songs[idx]["title"], score))
