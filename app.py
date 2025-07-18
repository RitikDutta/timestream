from flask import Flask, request, render_template, jsonify
from utils.timestream import Timestream
app = Flask(__name__)

timestream = Timestream()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
    else:  # GET request
        youtube_url = request.args.get('url')
    video_id = timestream.get_youtube_video_id(youtube_url)
    transcript = timestream.get_youtube_transcript(video_id)
    meaningful_timestamps = timestream.generate_meaningful_timestamps(transcript)
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return render_template('display.html', youtube_url=embed_url, transcript=meaningful_timestamps)

@app.route('/display_frame', methods=['GET', 'POST'])
def display_frame():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        print("youtube_url", youtube_url)
    else:  # GET request
        youtube_url = request.args.get('url')
    video_id = timestream.get_youtube_video_id(youtube_url)
    # video_id = 'tNrNLoCqzco'

    transcript = timestream.get_youtube_transcript(video_id)
    meaningful_timestamps = timestream.generate_meaningful_timestamps(transcript)
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return render_template('display_frame.html', youtube_url=embed_url, transcript=meaningful_timestamps)

@app.route('/reload_timestamps', methods=['POST'])
def reload_timestamps():
    video_id = request.json['video_id']
    video_id = video_id.split("embed/")[-1]
    print("ID::: ", video_id)
    transcript = timestream.get_youtube_transcript(video_id)
    meaningful_timestamps = timestream.generate_meaningful_timestamps(transcript)
    return jsonify(timestamps=meaningful_timestamps)

@app.route('/user_query', methods=['POST'])
def user_query_endpoint():
    data = request.get_json()
    print(data)
    youtube_url = data['video_id']
    video_id = timestream.get_youtube_video_id(youtube_url)
    user_query = data['user_query']
    
    # Get the transcript with your existing method
    transcript = timestream.get_youtube_transcript(video_id)
    # Use the user_query function defined in Timestream
    answer = timestream.user_query(transcript, user_query)
    
    print(f'ANSWER======================={answer}')
    # Return JSON response
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
