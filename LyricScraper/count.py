import json
with open("concatenated.json", "r") as f:
	songs2 = json.load(f)

artists = []
for song in songs2:
	if song["artist"] not in artists:
		artists.append(song["artist"])

print(sorted(artists))