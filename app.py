@app.route('/videos', methods=['POST'])
def download():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'No se proporcionó URL'}), 400

        carpeta = '/tmp/ssscatu'
        os.makedirs(carpeta, exist_ok=True)

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
