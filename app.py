import os
from flask import Flask, request, render_template, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

def get_instructions(instructions):
    with open(instructions, 'r') as file:
        instructions = file.read()
    return instructions
    
def get_youtube_transcript(video_id):
    transcript_text = []
    languages = ['en', 'hi']
    
    for language in languages:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
            print(f"Transcript found in language: {language}")
            for entry in transcript:
                start_time = format_time(entry['start'])
                text = entry['text']
                transcript_text.append(f"{start_time} {text}")
            return transcript_text  # Return if transcript is found
        except NoTranscriptFound:
            print(f"Transcript not found for language: {language}")
    
    raise NoTranscriptFound(f"Transcript not found for languages: {', '.join(languages)}")

    return transcript_text
def generate_meaningful_timestamps(transcript):
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
        system_instruction=get_instructions('instructions.txt')
    )

    chat_session = model.start_chat(history=[])

    # Send the transcript to the model
    response = chat_session.send_message("\n".join(transcript))
    cleaned_lines = []
    for line in response.text.splitlines():
        if line.strip():
            # Remove unwanted characters and clean the line
            cleaned_line = line.strip().strip("`").replace('*', '')
            cleaned_lines.append(cleaned_line)
    return cleaned_lines


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display():
    youtube_url = request.form['youtube_url']
    video_id = youtube_url.split("v=")[-1]
    transcript = get_youtube_transcript(video_id)
    meaningful_timestamps = generate_meaningful_timestamps(transcript)
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return render_template('display.html', youtube_url=embed_url, transcript=meaningful_timestamps)

@app.route('/reload_timestamps', methods=['POST'])
def reload_timestamps():
    video_id = request.json['video_id']
    video_id = video_id.split("embed/")[-1]
    print("ID::: ", video_id)
    transcript = get_youtube_transcript(video_id)
    meaningful_timestamps = generate_meaningful_timestamps(transcript)
    return jsonify(timestamps=meaningful_timestamps)

if __name__ == '__main__':
    app.run(debug=True)
