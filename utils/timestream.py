import os
from flask import Flask, request, render_template, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from dotenv import load_dotenv
import re
import requests

class Timestream:
    def __init__(self, api_key='AIzaSyDNOZ4XoQjFLPWMZ0cmIYc1w8nx3eYS8hg'):
        """
        Initializes the YouTubeTranscriptExtractor with the necessary API credentials.

        Parameters:
            api_key (str): The API key for authorization.
        """
        self.base_dir = os.path.abspath(os.path.dirname(__file__))

        self.url = "https://www.youtube-transcript.io/api/transcripts"
        self.headers = {
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
        }

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    def get_youtube_video_id(self, url):
        # Regex patterns for different YouTube URL formats
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        ]

        for pattern in patterns:
            match = re.match(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_instructions(self, instructions):
        with open(instructions, 'r') as file:
            instructions = file.read()
        return instructions
        
    def get_youtube_transcript(self, video_id):
        transcript_text = []
        languages = ['en', 'hi']
        print(f"----------{video_id}----------")
        for language in languages:
            try:

                YTA = YouTubeTranscriptApi()
                transcript = YTA.fetch(video_id, languages=[language])
                print(type(transcript))
                # print(transcript)
                print(f"Transcript found in language: {language}")
                for entry in transcript:
                    start_time = self.format_time(entry.start)
                    text = entry.text
                    transcript_text.append(f"{start_time} {text}")
                return transcript_text  # Return if transcript is found
            except NoTranscriptFound as e:
                print(f"Transcript not found for language: {language}")
        
        # If no transcript is found for any language, raise the exception with required arguments
        raise NoTranscriptFound(requested_language_codes=languages, transcript_data=None)

    #as youtube have blocked the api from ipv6 commonly used by cloud platforms so we did a different technique to get the transcript
    def get_youtube_transcript_different_api(self, video_id, preferred_language='English'):
        
        response_tr2 = self._make_api_request(video_id)
        if not response_tr2:
            print("Failed to retrieve transcript data.")
            return []

        # Step 2: Extract 'tracks' from the response
        try:
            tracks = response_tr2[0]['tracks']
        except (IndexError, KeyError) as e:
            print(f"Error extracting 'tracks' from response: {e}")
            return []

        # Step 3: Extract preferred language transcript
        transcript = self._extract_transcript_with_floats(tracks, preferred_language)

        # Step 4: If preferred language not found, fallback to alternative language
        if not transcript:
            fallback_language = 'Hindi (auto-generated)' if preferred_language.lower() == 'english' else 'English'
            print(f"Preferred language '{preferred_language}' not found. Falling back to '{fallback_language}'.")
            transcript = self._extract_transcript_with_floats(tracks, fallback_language)

            if not transcript:
                print(f"No transcript available for '{preferred_language}' or '{fallback_language}'.")
                return []

        # Step 5: Format the transcript entries
        transcript_text = []
        for entry in transcript:
            start_time = self._format_time(entry['start'])
            text = entry['text']
            transcript_text.append(f"{start_time} {text}")

        return transcript_text

    def _make_api_request(self, video_id):
        """
        Makes a POST request to the YouTube Transcript API to fetch transcript data.

        Parameters:
            video_id (str): The YouTube video ID.

        Returns:
            list or None: Parsed JSON response if successful; otherwise, None.
        """
        payload = {
            "ids": [video_id]
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code == 200:
                response_tr2 = response.json()
                print("Response successfully received and parsed!")
                # Uncomment the following line to see the full JSON response
                # print(json.dumps(response_tr2, indent=2))
                return response_tr2
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the API request: {e}")
            return None

    def _extract_transcript_with_floats(self, tracks, language):
        """
        Extracts the transcript for the specified language and converts 'start' and 'dur' to floats.

        Parameters:
            tracks (list): List of language blocks with transcripts.
            language (str): The language to extract (e.g., 'English' or 'Hindi (auto-generated)').

        Returns:
            list or None: List of transcript entries with 'start' and 'dur' as floats, or None if not found.
        """
        # Find the matching language block
        transcript = next(
            (track['transcript'] for track in tracks if track['language'].lower() == language.lower()),
            None
        )

        if transcript:
            # Convert 'start' and 'dur' to floats
            for entry in transcript:
                try:
                    entry.start = float(entry.get('start', 0))
                except ValueError:
                    entry.start = 0.0
                try:
                    entry.dur = float(entry.get('dur', 0))
                except ValueError:
                    entry.dur = 0.0
            return transcript
        else:
            return None

    def _format_time(self, seconds):
        """
        Converts seconds (float) to MM:SS string format.

        Parameters:
            seconds (float): Time in seconds.

        Returns:
            str: Formatted time string in "MM:SS" format.
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02}:{secs:02}"

    def generate_meaningful_timestamps(self, transcript):
        load_dotenv()
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-preview-04-17",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction=self.get_instructions(os.path.join(self.base_dir, 'instructions.txt'))
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
    


    def user_query(self, transcript, query):
        load_dotenv()
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 1000,
                "response_mime_type": "text/plain",
            },
            system_instruction=self.get_instructions(os.path.join(self.base_dir, 'query_instructions.txt'))
        )

        chat_session = model.start_chat(history=[])

        # Send the transcript to the model
        try:
            response = chat_session.send_message("\n".join(query) + " ".join(transcript) )
            cleaned_lines = []
            for line in response.text.splitlines():
                if line.strip():
                    # Remove unwanted characters and clean the line
                    cleaned_line = line.strip().strip("`").replace('*', '')
                    cleaned_lines.append(cleaned_line)
            return cleaned_lines
        except:
            response = "The Video is too long for Our model to go through"
            return response