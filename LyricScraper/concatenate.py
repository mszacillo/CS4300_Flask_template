import json

with open("scrapeddata.json", "r") as f:
	songs1 = json.load(f)

with open("concatenated.json", "r") as f:
	songs2 = json.load(f)

allsongs = songs1 + songs2

with open("concatenated.json", "w") as outfile:
		json.dump(allsongs, outfile)



