import os
import subprocess
import glob
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Carpeta de descargas
BASE_DIR = os.getcwd()
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "storage")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/descarga", methods=["POST"])
def descarga():
    url = request.form.get("url")
    formato = request.form.get("formato")  # 'video' o 'audio'

    if not url or not formato:
        return jsonify({"error": "Faltan datos"}), 400

    # Limpiar carpeta antes de descargar
    for f in os.listdir(DOWNLOAD_FOLDER):
        try:
            os.remove(os.path.join(DOWNLOAD_FOLDER, f))
        except Exception:
            pass

    try:
        cookies_path = os.path.join(BASE_DIR, "cookies.txt")

        if formato == "audio":
            cmd = [
                "yt-dlp",
                "--cookies", cookies_path,
                "--restrict-filenames",
                "-x",
                "--audio-format", "mp3",
                "-o", os.path.join(DOWNLOAD_FOLDER, "%(id)s.%(ext)s"),
                url
            ]
        else:
            cmd = [
                "yt-dlp",
                "--cookies", cookies_path,
                "--restrict-filenames",
                "-f", "mp4",
                "-o", os.path.join(DOWNLOAD_FOLDER, "%(id)s.%(ext)s"),
                url
            ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        archivos = glob.glob(os.path.join(DOWNLOAD_FOLDER, "*"))
        if not archivos:
            return jsonify({"error": "No se generó ningún archivo"}), 500

        return send_file(
            archivos[0],
            as_attachment=True
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
