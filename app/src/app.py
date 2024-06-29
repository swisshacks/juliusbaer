import os
from flask import Flask, request, render_template
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import joblib

from fake.analyse_fake import analyze_audio

app = Flask(__name__)

def extract_mfcc_features(audio_path, n_mfcc=13, n_fft=2048, hop_length=512):
    try:
        audio_data, sr = librosa.load(audio_path, sr=None)
    except Exception as e:
        print(f"Error loading audio file {audio_path}: {e}")
        return None

    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    return np.mean(mfccs.T, axis=0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "audio_file" not in request.files:
            return render_template("index.html", message="No file part")
        
        audio_file = request.files["audio_file"]
        if audio_file.filename == "":
            return render_template("index.html", message="No selected file")
        
        if audio_file and allowed_file(audio_file.filename):
            if not os.path.exists("uploads"):
                os.makedirs("uploads")
                
            audio_path = os.path.join("uploads", audio_file.filename)
            audio_file.save(audio_path)
            result = analyze_audio(audio_path)
            print(result)
            os.remove(audio_path) 
            return render_template("result.html", result=result)
        
        return render_template("index.html", message="Invalid file format. Only .wav files allowed.")
    
    return render_template("index.html")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "wav"

if __name__ == "__main__":
    app.run(debug=True)
