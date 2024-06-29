from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from main import analyse_audio

app = Flask(__name__)

# Specify the path for saving uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16 Megabytes max file size

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


# Route to serve images
@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory('images', filename)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and file.filename.endswith('.wav'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        # PAth to absolute path
        file_path = os.path.abspath(file_path)
        print(file_path)
        fake, wrong_info, impostor, name = analyse_audio(file_path)
        print(fake, wrong_info, impostor, name)
        print(f"Type of fake: {type(fake)}")
        print(f"Type of wrong_info: {type(wrong_info)}")
        print(f"Type of impostor: {type(impostor)}")
        print(f"Type of name: {type(name)}")
        return jsonify({'fake': fake, 'wrong_info': wrong_info, 'impostor': impostor, 'name': name})
    
    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
