from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import yt_dlp
import uuid

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>ssscatu</title>
      <style>
        body { font-family: sans-serif; padding: 20px; text-align: center; background: #f0f0f0; }
        input, button { padding: 10px; font-size: 16px; width: 90%; max-width: 400px; margin: 10px 0; }
      </style>
    </head>
    <body>
      <h1>Descargar video</h1>
      <input type="text" id="url" placeholder="Enlace del video">
      <button onclick="enviar()">Descargar</button>
      <p id="estado"></p>
      <script>
        function enviar() {
          const url = document.getElementById('url').value;
          const estado = document.getElementById('estado');
          estado.innerText = 'Enviando...';
          fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
          })
          .then(res => res.json())
          .then(data => {
            if (data.link) {
              estado.innerHTML = 'Video descargado: <a href="' + data.link + '" target="_blank">Descargar aquí</a>';
            } else {
              estado.innerText = data.error;
            }
          })
          .catch(() => estado.innerText = 'Error de red o conexión');
        }
      </script>
    </body>
    </html>
    '''

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400

    unique_id = str(uuid.uuid4())
    filepath = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.mp4")

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': filepath,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'link': f'/video/{unique_id}.mp4'})
    except Exception as e:
        return jsonify({'error': f'Error al descargar: {str(e)}'}), 500

@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
