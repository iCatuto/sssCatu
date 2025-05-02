from flask import Flask, request, jsonify, send_file, render_template_string
import subprocess
import os
import uuid

app = Flask(__name__)

# Carpeta segura de descargas dentro del entorno de Render
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# HTML simple para probar la app
HTML = """
<!doctype html>
<html>
  <head><title>Descargar Multimedia</title></head>
  <body>
    <h1>Descargar TikTok / YouTube / Spotify</h1>
    <form method="post" action="/descarga">
      <input name="url" type="text" placeholder="Enlace..." required>
      <button type="submit">Descargar</button>
    </form>
  </body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/descarga", methods=["POST"])
def descarga():
    url = request.form.get("url")
    if not url:
        return jsonify({"error": "Falta la URL"}), 400

    filename = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    # Detecta si es Spotify
    if "spotify.com" in url:
        cmd = ["spotdl", "--path-template", output_path, url]
    else:
        cmd = ["yt-dlp", "-o", f"{output_path}.%(ext)s", url]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        # Encuentra archivo descargado
        for fname in os.listdir(DOWNLOAD_DIR):
            if fname.startswith(filename):
                return send_file(os.path.join(DOWNLOAD_DIR, fname), as_attachment=True)

        return jsonify({'error': 'Archivo no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Configurar el puerto para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
