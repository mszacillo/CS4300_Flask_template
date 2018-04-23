from __future__ import print_function
import numpy as np
import json
from scipy.sparse.linalg import svds

def init():
	global song_transcripts_global
	with open("./app/helper_functions/songData.json", "r") as f:
		song_transcripts_global = json.load(f)