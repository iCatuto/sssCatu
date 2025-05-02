import os
import subprocess
import uuid
import glob
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Carpeta para guardar archivos
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'storage')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descarga', methods=['POST'])
def descarga():
    url = request.form.get('url')

    if not url:
        return jsonify({'error': 'Falta la URL'}), 400

    try:
        # Limpiar carpeta antes de cada descarga
        for f in os.listdir(DOWNLOAD_FOLDER):
            os.remove(os.path.join(DOWNLOAD_FOLDER, f))

        # Descargar el contenido (Spotify o video) con yt-dlp
        cmd = ['yt-dlp', '-P', DOWNLOAD_FOLDER, url]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        # Buscar archivos descargados
        archivos = glob.glob(os.path.join(DOWNLOAD_FOLDER, '*'))
        if not archivos:
            return jsonify({'error': 'No se encontró el archivo'}), 500

        return send_file(archivos[0], as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
