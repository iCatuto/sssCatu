import os
import subprocess
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Carpeta de descargas
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

    try:
        if tipo == 'musica':
            cmd = ['spotdl', url, '--output', DOWNLOAD_FOLDER]
        else:
            output_template = os.path.join(DOWNLOAD_FOLDER, f'%(title)s.%(ext)s')
            cmd = ['yt-dlp', '-o', output_template, url]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        return jsonify({'mensaje': 'Descarga completada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para servir archivos descargados (opcional)
@app.route('/descargas/<path:filename>')
def descargar_archivo(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
