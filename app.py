from flask import Flask, render_template, request, send_file, redirect, url_for
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        quality = request.form["quality"]
        uid = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_FOLDER, f"{uid}.%(ext)s")

        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'outtmpl': output_template,
            'merge_output_format': 'mp4'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            video_path = output_template.replace("%(ext)s", "mp4")
            return send_file(video_path, as_attachment=True)

        except Exception as e:
            return f"Erro ao baixar o vídeo: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
