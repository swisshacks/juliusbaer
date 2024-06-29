import os
import json
import csv
import spacy
import jellyfish
import unicodedata
from fuzzywuzzy import fuzz
from collections import Counter
from groq import Groq
import pandas as pd

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

def normalize_name(name):
	name = name.lower()
	name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
	name = name.replace('-', ' ').replace("'", '')
	return ' '.join(name.split())

def name_similarity(name1, name2):
	name1 = normalize_name(name1)
	name2 = normalize_name(name2)
	
	jaro_winkler = jellyfish.jaro_winkler_similarity(name1, name2)
	levenshtein = jellyfish.levenshtein_distance(name1, name2)
	soundex_similarity = int(jellyfish.soundex(name1) == jellyfish.soundex(name2))
	
	parts1 = set(name1.split())
	parts2 = set(name2.split())
	common_parts = len(parts1.intersection(parts2))
	
	# Calculate a weighted score
	score = (jaro_winkler * 0.4 + 
			(1 - levenshtein / max(len(name1), len(name2))) * 0.3 +
			soundex_similarity * 0.1 +
			common_parts / max(len(parts1), len(parts2)) * 0.2)
	
	return score

def extract_names(text):
	print(text)
	doc = nlp(text)
	return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

def match_client_profile(names, client_profiles, threshold=0.8):
	best_match = None
	best_score = 0
	for name in names:
		for profile in client_profiles:
			score = name_similarity(name, profile['name'])
			if score > best_score:
				best_score = score
				best_match = profile

	if best_score >= threshold:
		return best_match, best_score
	else:
		return None, best_score

def load_client_profiles(csv_path):
	client_profiles = []
	with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			client_profiles.append(row)
	return client_profiles

def groq_get_name(transcript, profiles):
	client = Groq(
		api_key="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",
	)

	# give the transcript
	# specify the format (json typically)
	# and give examples
	# ask it to justify answers (as a second check)
	# parse the json
	if transcript:
		check = client.chat.completions.create(
			messages=[
				{
					"role": "user",
					"content": f" \
					You are provided with a call transcript and client profiles. Your task is to identify the client \
					from whom the transcript originated. Ensure to use the exact name from the profiles when making a match. \
					ONLY reponsd with ONE of the NAMES provided \
					Here are the files for your review: \
					NAMES: Amina Kouri, Santiago Rivera, Chen Wei, Elena Popova, Liam O'Brien, Anika Patel, Hiroshi Nakamura, Noah Zimmerman, Isabella Rossi, Mia Anderson, Olivia Tremblay, Sofia Almeida, Elias Svensson, Fatima Zahra Mansouri, Seo-yun Kim, Lara van den Berg, Finn Murphy, Kai Løkke,Jorge Castillo, Charlotte Leclerc \
					transcript: {transcript}"
				}
			],
			model="llama3-70b-8192"
		)
		res = check.choices[0].message.content.strip()
		return res

def load_file(filename):
	# print(filename)
	if not filename.endswith('.json'):
		return False
	file_path = os.path.join(json_folder, filename)
	with open(file_path, 'r', encoding='utf-8') as file:
		data = json.load(file)
		fulltext = data['result'].get('translated_text', '')
		return fulltext

def process_transcript(filename, client_profiles):
	results = Counter()
	successes = []
	failures = []

	# for filename in os.listdir(json_folder):
	json_folder = '../audio_clips'
	try:
		# print(filename)
		file_path = os.path.join(json_folder, filename)
		print(file_path)
		# print(file_path)
		# fulltext = load_file(file_path)
		with open(file_path, 'r', encoding='utf-8') as file:
			data = json.load(file)
			fulltext = data['result'].get('translated_text', '')
	except:
		print("Error")

	names = extract_names(fulltext[:500])
	print(names)

	def get_from_groq(fulltext, client_profiles):
		name_from_groq = groq_get_name(fulltext, client_profiles)
		if name_from_groq:
			return name_from_groq
		else :
			print("Waiting 20 seconds and trying again")
			sleep(65)
			name_from_groq = groq_get_name(fulltext, client_profiles)
			if name_from_groq:
				return name_from_groq
			else:
				print("GROQ fail twice")
				return None

	if names:
		matched_profile, score = match_client_profile(names, client_profiles)
		if matched_profile:
			results['success'] += 1
			successes.append((filename[:-5], ', '.join(names)))
			names_str = ', '.join(names)
			return names_str
		else:
			print("No match")
			name_from_groq = get_from_groq(fulltext, client_profiles)
			return name_from_groq
			if name_from_groq:
				results['success'] += 1
				successes.append((filename[:-5], name_from_groq))
	else:
		name_from_groq = get_from_groq(fulltext, client_profiles)
		return name_from_groq
		if name_from_groq:
			results['success'] += 1
			successes.append((filename[:-5], name_from_groq))
		else:
			results['success'] += 1
			successes.append((filename[:-5], 'No name'))

	return results, failures

def process_transcripts(json_folder, client_profiles):
	results = Counter()
	successes = []
	failures = []

	for filename in os.listdir(json_folder):
		try:
			#if json
			if not filename.endswith('.json'):
				continue
			# print(filename)
			file_path = os.path.join(json_folder, filename)
			# print(file_path)
			# fulltext = load_file(file_path)
			with open(file_path, 'r', encoding='utf-8') as file:
				data = json.load(file)
				fulltext = data['result'].get('translated_text', '')
		except:
			print("Error")
			continue

		names = extract_names(fulltext[:500])
		print(names)

		def get_from_groq(fulltext, client_profiles):
			name_from_groq = groq_get_name(fulltext, client_profiles)
			if name_from_groq:
				return name_from_groq
			else :
				print("Waiting 20 seconds and trying again")
				sleep(65)
				name_from_groq = groq_get_name(fulltext, client_profiles)
				if name_from_groq:
					return name_from_groq
				else:
					print("GROQ fail twice")
					return None

		if names:
			matched_profile, score = match_client_profile(names, client_profiles)
			if matched_profile:
				results['success'] += 1
				successes.append((filename[:-5], ', '.join(names)))
			else:
				print("No match")
				name_from_groq = get_from_groq(fulltext, client_profiles)
				if name_from_groq:
					results['success'] += 1
					successes.append((filename[:-5], name_from_groq))
		else:
			name_from_groq = get_from_groq(fulltext, client_profiles)
			if name_from_groq:
				results['success'] += 1
				successes.append((filename[:-5], name_from_groq))
			else:
				results['success'] += 1
				successes.append((filename[:-5], 'No name'))
					

	with open('matched_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['rec_id', 'name'])
		writer.writerows(successes)
	
	# Print summary after processing all files
	print(f"Successes: {results['success']}")
	print(f"Failures: {results['failure']}")
	print(f"No names extracted: {results['no_name']}")
	print(f"Errors: {results['error']}")

	# Print failures after processing all files
	print("\nFailures:")
	for failure in failures:
		print(f"File: {failure[0]}, Name: {failure[1]}, Score: {failure[2]:.2f}")

	return results, failures

# File paths
# json_folder = '/home/jolivier/juliusbaer/audio_clips'
# client_profiles_path = '/home/jolivier/juliusbaer/client_profiles/client_features.csv'

# # Load client profiles from CSV
# client_profiles = load_client_profiles(client_profiles_path)

# # Process transcripts
# process_transcripts(json_folder, client_profiles)

# # Load client profiles from CSV
from Levenshtein import distance as levenshtein_distance

# # Assuming df_profiles is already loaded and 'names' list is created as shown
# df_profiles = pd.read_csv('../client_profiles/client_features.csv')
# names = df_profiles['name'].tolist()

# # Load client profiles from CSV
# client_profiles = pd.read_csv('matched_results.csv')

# Function to filter names based on the 'names' list with a tolerance for one letter difference
def find_single_closest_match(name_string, names):
    # Split the string by commas and strip extra whitespace
    split_names = [name.strip() for name in name_string.split(',')]
    # Initialize a variable to hold the closest overall match and its minimum distance found so far
    closest_overall_match = None
    min_distance = float('inf')  # Start with a very high number

    # Loop through each split name to find the single closest match
    for name in split_names:
        # For each name, find the name from 'names' with the minimum Levenshtein Distance
        for n in names:
            current_distance = levenshtein_distance(name, n)
            if current_distance < min_distance:
                min_distance = current_distance
                closest_overall_match = n

    # Return the single closest match found for the entire name string
    return closest_overall_match

# # Apply the function to the 'name' column of client_profiles
# client_profiles['name'] = client_profiles['name'].apply(find_single_closest_match)

# # save
# client_profiles.to_csv('filtered_matched_results.csv', index=False)

# df = pd.read_csv('matched_results.csv')
# print(df.head())

# # df['name'] = df['name'].str.split(',').str[0]

# #if the sentence is more than 4 words, extract_names
# df['name'] = df.apply(lambda x: extract_names(x['name']) if len(x['name'].split())> 4 else x['name'], axis=1)



# #save to csv
# df.to_csv('matched_results.csv', index=False)

