import os
import subprocess
import glob
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'storage')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descarga', methods=['POST'])
def descarga():
    url = request.form.get('url')
    formato = request.form.get('formato')

    if not url or not formato:
        return jsonify({'error': 'Faltan datos'}), 400

    for f in os.listdir(DOWNLOAD_FOLDER):
        os.remove(os.path.join(DOWNLOAD_FOLDER, f))

    try:
        cookies_path = os.path.join(os.getcwd(), 'cookies.txt')

        if formato == 'audio':
            cmd = [
                'yt-dlp',
                '--cookies', cookies_path,
                '--restrict-filenames',
                '-x', '--audio-format', 'mp3',
                '-o', os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
                url
            ]
        else:
            cmd = [
                'yt-dlp',
                '--cookies', cookies_path,
                '--restrict-filenames',
                '-f', 'mp4',
                '-o', os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
                url
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        archivos = glob.glob(os.path.join(DOWNLOAD_FOLDER, '*'))
        if not archivos:
            return jsonify({'error': 'No se encontró el archivo'}), 500

        return send_file(archivos[0], as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
