from flask import Flask, request, render_template, redirect, url_for
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

app = Flask(__name__)

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

def get_youtube_transcript(video_id, language='en'):
    transcript_text = []
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        for entry in transcript:
            start_time = format_time(entry['start'])
            text = entry['text']
            transcript_text.append(f"{start_time} {text}")
    except NoTranscriptFound:
        transcript_text.append(f"Transcript not found for the language '{language}'.")
    except Exception as e:
        transcript_text.append(f"An error occurred: {e}")
    return transcript_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display():
    youtube_url = request.form['youtube_url']
    video_id = youtube_url.split("v=")[-1]
    transcript = get_youtube_transcript(video_id)
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return render_template('display.html', youtube_url=embed_url, transcript=transcript)

if __name__ == '__main__':
    app.run(debug=True)
