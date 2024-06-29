
from src.fake.predict import analyze_audio
from src.impersonator.predict import analyse_is_impersonator

from src.message_func import process_transcript, find_single_closest_match, load_client_profiles

import os
import numpy as np
import pandas as pd

#reload automatically the modules
import importlib
import sys

def analyse_audio(audio_path):
	# CHECK IS_FAKE AUDIO#
	print(audio_path)
	is_fake = analyze_audio(audio_path)
	# is_fake = "True" if is_fake else "False"
	print(f"Is the audio fake? {is_fake}\n")

	#CHECK
	id_audio = os.path.basename(audio_path).split(".")[0]
	print(id_audio)
	audio_json = id_audio + ".json"
	audio_json_path = os.path.join("/home/jolivier/juliusbaer/audio_clips", audio_json)
	client_profiles_path = '/home/jolivier/juliusbaer/client_profiles/client_features.csv'
	client_profiles = load_client_profiles(client_profiles_path)
 
	name = process_transcript(audio_json, client_profiles)
	df_profiles = pd.read_csv('../client_profiles/client_features.csv')
	names = df_profiles['name'].tolist()
	name_filtered = find_single_closest_match(name, names)
	# name_filtered = "Jorge Castillo"
	print(f"Name: {name_filtered}\n")

	is_impersonator = analyse_is_impersonator(audio_path, name_filtered)
	# is_impersonator = "True" if is_impersonator else "False"
	print(f"Is the audio impersonator? {is_impersonator}\n")
 
	return is_fake, 0, is_impersonator, name_filtered

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Please provide the path to the audio file as an argument.")
		sys.exit(1)
	audio_path = sys.argv[1]
	is_fake, _, is_impersonator, name_filtered = analyse_audio(audio_path)
	print(is_fake, is_impersonator, name_filtered)
	# Do something with the results