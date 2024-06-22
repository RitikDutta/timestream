import os
from flask import Flask, request, render_template, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from dotenv import load_dotenv

class Timestream:
    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    def get_instructions(self, instructions):
        with open(instructions, 'r') as file:
            instructions = file.read()
        return instructions
        
    def get_youtube_transcript(self, video_id):
        transcript_text = []
        languages = ['en', 'hi']
        
        for language in languages:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
                print(f"Transcript found in language: {language}")
                for entry in transcript:
                    start_time = self.format_time(entry['start'])
                    text = entry['text']
                    transcript_text.append(f"{start_time} {text}")
                return transcript_text  # Return if transcript is found
            except NoTranscriptFound as e:
                print(f"Transcript not found for language: {language}")
        
        # If no transcript is found for any language, raise the exception with required arguments
        raise NoTranscriptFound(requested_language_codes=languages, transcript_data=None)

    def generate_meaningful_timestamps(self, transcript):
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
            system_instruction=self.get_instructions('timestream/utils/instructions.txt')
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
