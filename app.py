from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return '''
    <h1>ssscatu</h1>
    <form method="POST" action="/descargar" enctype="application/x-www-form-urlencoded">
        <input name="url" placeholder="URL de video o canción" required>
        <select name="tipo">
            <option value="video">Video</option>
            <option value="spotify">Spotify</option>
        </select>
        <button type="submit">Descargar</button>
    </form>
    '''

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form.get("url")
    tipo = request.form.get("tipo")

    if not url or not tipo:
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        if tipo == "video":
            opciones = {
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'format': 'mp4',
            }
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return jsonify({'success': f'Video descargado: {filename}'})

        elif tipo == "spotify":
            comando = ["spotdl", url, "--output", DOWNLOAD_DIR]
            resultado = subprocess.run(comando, capture_output=True, text=True)
            if resultado.returncode == 0:
                return jsonify({'success': 'Canción descargada con SpotDL'})
            else:
                return jsonify({'error': f'Error en SpotDL: {resultado.stderr}'})
        else:
            return jsonify({'error': 'Tipo no reconocido'}), 400

    except Exception as e:
        return jsonify({'error': f'Error al descargar: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
