import pandas as pd
import scipy.io.wavfile as wav
from sklearn.mixture import GaussianMixture
from python_speech_features import mfcc
import os
import numpy as np
import librosa
import torch
import whisper
import scipy.io.wavfile as wav


model = whisper.load_model("tiny")

PATH = r'app\\src\\impersonator\\gmms\\'
files_in_path = os.listdir(PATH)
names = set([file.split('_')[1] for file in files_in_path])
gmms = {name: GaussianMixture(n_components = 3) for name in names}
for name in names:
	gmm_name = PATH + 'gmm_' + name
	means = np.load(gmm_name + '_means.npy')
	covar = np.load(gmm_name + '_covariances.npy')
	gmms[name].precisions_cholesky_ = np.load(gmm_name + '_precisions_cholesky.npy')
	gmms[name].weights_ = np.load(gmm_name + '_weights.npy')
	gmms[name].means_ = means
	gmms[name].covariances_ = covar


@torch.no_grad()
def extract_features(audio_path, 
                     model,
                     target_sr = 16_000):
	
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    y, sr = librosa.load(audio_path, sr=None)
    if sr != target_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)

    y = y / np.max(np.abs(y))
    valid_share = y.shape[0]

    y = whisper.pad_or_trim(y)
    valid_share /= y.shape[0]
    mel = whisper.log_mel_spectrogram(y)
    mel = mel.unsqueeze(0).to(device)
    features = model.embed_audio(mel)
    
    return features[0, :int(valid_share * 1500) + 1:10, :].cpu()


def get_likelihoods(audio_path, gmms, model):

    likelihoods = {name: None for name in gmms.keys()}

    for name, gmm in gmms.items():
        features = extract_features(audio_path, model)
        likelihoods[name] = gmm.score(features)

    return likelihoods


def analyze(audio_path, gmms, claimed_name, model):
    
        likelihoods = get_likelihoods(audio_path, gmms, model)
        
        highest_likelihood = max(likelihoods.values())
        best_match = [name for name, likelihood in likelihoods.items() if likelihood == highest_likelihood][0]

        if claimed_name == best_match:
            return 0
        else:
            return 1


def coucou():
	print("coucou")


def analyse_is_impersonator(audio_file, actual_name):

    return analyze(audio_file, gmms, actual_name, model)
