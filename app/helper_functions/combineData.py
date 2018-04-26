import json
import random

with open("songData.json", "r") as f:
	songs1 = json.load(f)

with open("concatenated.json", "r") as f:
	songs2 = json.load(f)

keyset = songs1.keys()
for song in songs2:
	randomint = random.randint(1, 1500000)
	if randomint not in keyset:
		songs1[str(randomint)] = song

with open("entireData.json", "w") as outfile:
		json.dump(songs1, outfile)

