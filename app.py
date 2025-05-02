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
    url = request.form.get('url')
    tipo = request.form.get('tipo')

    if not url or not tipo:
        return jsonify({'error': 'Faltan datos'}), 400

    filename = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{filename}.%(ext)s")

    try:
        if tipo == 'musica':
            cmd = ['spotdl', 'download', url, '--output', DOWNLOAD_FOLDER]
        else:
            cmd = ['yt-dlp', '-o', output_path, url]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        return jsonify({'mensaje': 'Descarga completada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Esto debe estar totalmente fuera del bloque try-except
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
