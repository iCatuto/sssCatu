from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import yt_dlp
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>ssscatu</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          padding: 20px;
          background: #f4f4f4;
          text-align: center;
        }
        input, button {
          font-size: 16px;
          padding: 10px;
          margin: 10px auto;
          width: 100%;
          max-width: 400px;
        }
        #estado {
          margin-top: 20px;
          font-weight: bold;
        }
      </style>
    </head>
    <body>
      <h1>ssscatu</h1>
      <input type="text" id="url" placeholder="Pega el enlace aquí">
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
            estado.innerText = data.success || data.error;
          })
          .catch(() => {
            estado.innerText = 'Error de red o conexión';
          });
        }
      </script>
    </body>
    </html>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No se proporcionó URL'}), 400

    download_dir = os.path.join("/tmp", "downloads", str(uuid.uuid4()))
    os.makedirs(download_dir, exist_ok=True)

    try:
        if "spotify.com" in url:
            result = subprocess.run(
                ["spotdl", url, "--output", download_dir],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return jsonify({'error': result.stderr}),
