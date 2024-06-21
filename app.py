import os
from flask import Flask, request, render_template
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
        system_instruction="To ensure the AI generates precise timestamps that align closely with the actual topics in the video, follow these improved instructions:\n\n### Instructions for Generating Accurate YouTube Timestamps\n\nwrite transcript in English\n\n1. **Start with 0:00**: Begin the first timestamp at 0:00 to indicate the start of the video.\n\n2. **Short Titles**: Keep each timestamp title concise, ideally no more than 5 words. Ensure titles are clear and descriptive.\n\n3. **Key Points Only**: Focus on significant points and transitions within the video. Avoid adding timestamps for minor details.\n\n4. **Consistent Format**: Use a consistent format for all timestamps. The structure should be:\n\n   [Time] - [Title]\n\n   Example: \n   0:00 - Introduction\n   1:15 - Key Concept 1\n   3:30 - Example Demonstration\n\n5. **Logical Segmentation**: Segment the video logically, ensuring each timestamp represents a distinct section or topic.\n\n6. **Clarity and Relevance**: Ensure each title is relevant to the content at that point in the video and provides viewers with a clear idea of what to expect.\n\n7. **Avoid Redundancy**: Do not repeat similar timestamps. Each timestamp should introduce new information or a new segment.\n\n8. **Even Distribution**: While not strictly necessary, aim for an even distribution of timestamps throughout the video to enhance navigation.\n\n9. **Verify Accuracy**: Double-check the timestamps against the video content to ensure they match correctly with the points being discussed.\n\n10. **Refine Timing**: After generating the initial timestamps, manually verify and adjust them to ensure they align perfectly with the actual topics. Pay attention to the exact start of each section or topic.\n\n### Example Template\n\n0:00 - Introduction\n1:15 - Overview\n3:30 - Topic 1\n6:00 - Topic 2\n8:45 - Key Takeaways\n10:00 - Conclusion\n"
    )

    chat_session = model.start_chat(history=[])

    # Send the transcript to the model
    response = chat_session.send_message("\n".join(transcript))
    cleaned_lines = []
    for line in response.text.splitlines():
        if line.strip():
            cleaned_lines.append(line.strip().strip("`"))
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

if __name__ == '__main__':
    app.run(debug=True)
