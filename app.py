from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import os
import subprocess
import uuid

app = Flask(__name__)
CORS(app)

HTML = """
<!doctype html>
<html>
  <head>
    <title>Descargador</title>
  </head>
  <body>
    <h1>Descargar Video o Música</h1>
    <form action="/descarga" method="post">
      <input type="text" name="url" placeholder="URL del video o canción" required>
      <select name="tipo">
        <option value="video">Video (yt-dlp)</option>
        <option value="musica">Música (Spotify - spotDL)</option>
      </select>
      <button type="submit">Descargar</button>
    </form>
  </body>
</html>
"""

@app.route("/")
def inicio():
    return render_template_string(HTML)

@app.route("/descarga", methods=["POST"])
def descarga():
    url = request.form.get("url")
    tipo = request.form.get("tipo", "video")

    if not url:
        return jsonify({"error": "Falta la URL"}), 400

    carpeta = os.path.join(os.getcwd(), "descargas")
    os.makedirs(carpeta, exist_ok=True)

    filename = str(uuid.uuid4())

    try:
        if tipo == "video":
            output = os.path.join(carpeta, f"{filename}.%(ext)s")
            cmd = ["yt-dlp", "-o", output, url]
        elif tipo == "musica":
            cmd = ["spotdl", "--output", carpeta, url]
        else:
            return jsonify({"error": "Tipo inválido"}), 400

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        archivos = os.listdir(carpeta)
        archivos.sort(key=lambda x: os.path.getmtime(os.path.join(carpeta, x)), reverse=True)
        ultimo = archivos[0]
        ruta_completa = os.path.join(carpeta, ultimo)

        return send_file(ruta_completa, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
