import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.manifold import TSNE

#%matplotlib inline

with open("songData.json", "r") as f:
	song_transcripts = json.load(f)

songs = list(song_transcripts.values())
print(songs[0].keys())

vectorizer = TfidfVectorizer(stop_words = "english", max_df = 0.7, min_df = 75)
lyric_matrix = vectorizer.fit_transform([song["lyrics"] for song in songs]).transpose()

u, s, v = svds(lyric_matrix, k=100)

# plt.plot(s[::-1])
# plt.xlabel("singular value number")
# plt.ylabel("Singular value")
# plt.show()

words_compressed, _, docs_compressed = svds(lyric_matrix, k = 40)
docs_compressed = docs_compressed.transpose()

print(words_compressed.shape)
print(docs_compressed.shape)

word_to_index = vectorizer.vocabulary_
print(word_to_index)
index_to_word = {i:t for t,i, in word_to_index.items()}
words_compressed = normalize(words_compressed, axis =1)

tsne = TSNE(verbose=1)
projected_docs = tsne.fit_transform(docs_compressed)
# print(projected_docs.shape)
# plt.figure(figsize=(15,15))
# plt.scatter(projected_docs[:,0], projected_docs[:,1])
# plt.show()

docs_compressed = normalize(docs_compressed, axis=1)

def closest_songs(project_index_in, k=10):
	sims = docs_compressed.dot(docs_compressed[project_index_in,:])
	asort = np.argsort(-sims)[:k+1]
	return [(songs[i]["title"], sims[i]/sims[asort[0]]) for i in asort[1:]]

for i in range(10):
	print(songs[i]["title"])
	for title, score in closest_songs(i):
		print("{}:{:.3f}".format(title[:40], score))
	print()


