@app.route("/descarga", methods=["POST"])
def descarga():
    try:
        url = request.json.get("url")
        if not url:
            return jsonify({"error": "URL no proporcionada"}), 400

        carpeta = os.path.join("downloads", str(uuid.uuid4()))
        os.makedirs(carpeta, exist_ok=True)

        if "spotify.com" in url:
            command = [
                "spotdl",
                url,
                "--output", os.path.join(carpeta, "%(title)s.%(ext)s")
            ]
        else:
            command = [
                "yt-dlp",
                "-o", os.path.join(carpeta, "%(title)s.%(ext)s"),
                url
            ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            archivos = os.listdir(carpeta)
            return jsonify({
                "mensaje": "Descarga exitosa",
                "archivos": archivos
            })
        else:
            return jsonify({"error": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
