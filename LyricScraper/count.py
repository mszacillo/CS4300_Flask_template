import json
with open("concatenated.json", "r") as f:
	songs2 = json.load(f)

noduplicates = []
songartists = []

for song in songs2:
	if song["artist"] not in songartists:
		songartists.append(song["artist"])

print(sorted(songartists))

# print(len(songs2))
# for song in songs2:
# 	currentsong = song["artist"] + song["title"]
# 	if currentsong not in songartists:
# 		noduplicates.append(song)

#print(sorted(artists))
# print(len(noduplicates))

# with open("concatenated.json", "w") as outfile:
# 		json.dump(songs2, outfile)