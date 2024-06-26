from flask import Flask, request, render_template, jsonify
from utils.timestream import Timestream
app = Flask(__name__)

timestream = Timestream()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display():
    youtube_url = request.form['youtube_url']
    video_id = youtube_url.split("v=")[-1]
    transcript = timestream.get_youtube_transcript(video_id)
    meaningful_timestamps = timestream.generate_meaningful_timestamps(transcript)
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return render_template('display.html', youtube_url=embed_url, transcript=meaningful_timestamps)

@app.route('/reload_timestamps', methods=['POST'])
def reload_timestamps():
    video_id = request.json['video_id']
    video_id = video_id.split("embed/")[-1]
    print("ID::: ", video_id)
    transcript = timestream.get_youtube_transcript(video_id)
    meaningful_timestamps = timestream.generate_meaningful_timestamps(transcript)
    return jsonify(timestamps=meaningful_timestamps)

if __name__ == '__main__':
    app.run(debug=True)
