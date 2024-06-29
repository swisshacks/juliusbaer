import pandas as pd
import scipy.io.wavfile as wav
from sklearn.mixture import GaussianMixture
from python_speech_features import mfcc
import os
import numpy as np

def extract_features(audio_path, trim_length=None):
	print(audio_path)
	sr, y = wav.read(audio_path)
	if trim_length:
		y = y[:trim_length * sr]  # multiplying by sr to convert seconds to samples
	mfccs = mfcc(y, sr, numcep=13)
	return mfccs

def train_gmm(features, n_components=3):
	gmm = GaussianMixture(n_components=n_components)
	gmm.fit(features)
	return gmm

def load_and_process_audio(file_path):
	features = extract_features(file_path)
	return features

def coucou():
	print("coucou")

def analyse_is_impersonator(audio_file, actual_name):
	# Directory containing the training audio files
	directory = "real_audio"
	# Load client profiles
	client_profiles = pd.read_csv("../client_profiles/real_match_name.csv")
	# Create a dictionary mapping rec_ids to file paths and client names
	audio_files = {row['rec_id']: (os.path.join(directory, row['rec_id'] + '.wav'), row['name'])
				for _, row in client_profiles.iterrows() if os.path.isfile(os.path.join(directory, row['rec_id'] + '.wav'))}

	gmms = {}
	for rec_id, (file_path, name) in audio_files.items():
		features = load_and_process_audio(file_path)
		gmm = train_gmm(features)
		gmms[rec_id] = gmm

	# Compare results
	results = []
	# Get the best match
	best_match = None
	features = load_and_process_audio(audio_file)
	best_score = -np.inf
	for rec_id, gmm in gmms.items():
		score = gmm.score(features)
		if score > best_score:
			best_score = score
			best_match = rec_id
	best_match_name = audio_files[best_match][1]
	match_result = actual_name == best_match_name
	#to num 
	match_result = 0 if match_result else 1
	return match_result
