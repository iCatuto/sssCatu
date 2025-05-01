from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def inicio():
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
        h1 {
          margin-bottom: 30px;
        }
        input, button {
          font-size: 16px;
          padding: 10px;
          margin-top: 10px;
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
      <input type="text" id="url" placeholder="Pega el enlace del video aquí">
      <button onclick="enviar()">Enviar al servidor</button>
      <p id="estado"></p>

      <script>
        function enviar() {
          const url = document.getElementById('url').value;
          const estado = document.getElementById('estado');
          estado.innerText = 'Enviando...';

          fetch('/download', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
          })
          .then(res => res.json())
          .then(data => {
            estado.innerText = data.success || data.error;
          })
          .catch(err => {
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

    carpeta = "/storage/emulated/0/Download/ssscatu"
    os.makedirs(carpeta, exist_ok=True)

    try:
        ydl_opts = {
            'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
            'format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({'success': f'Video descargado: {filename}'})
    except Exception as e:
        return jsonify({'error': f'Error al descargar: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
