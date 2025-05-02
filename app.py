import os
import subprocess
import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta a la carpeta de descargas
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'storage')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descarga', methods=['POST'])
def descarga():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No se proporcionó una URL'}), 400

    filename = f"{uuid.uuid4()}"
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{filename}.%(ext)s")

    try:
        if 'spotify.com' in url:
            cmd = ['spotdl', 'download', url, '--output', DOWNLOAD_FOLDER]
        else:
            cmd = ['yt-dlp', '-o', output_path, url]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        return jsonify({'mensaje': 'Descarga completada.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
