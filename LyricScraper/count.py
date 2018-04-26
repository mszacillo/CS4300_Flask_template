import json
with open("concatenated.json", "r") as f:
	songs2 = json.load(f)

print(len(songs2))