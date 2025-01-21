# -*- coding: utf-8 -*-
import json

def convert_to_subtitle_dicts(
    raw_json_str: str,
    language: str = 'en'
) -> list:
    """
    Convert the raw JSON string (YouTube-like response) into a list of dicts:
    [
      {"text": str, "start": float, "duration": float},
      ...
    ]
    based on the specified language track.

    :param raw_json_str: The entire JSON response as a string.
    :param language: 'en' (English) or 'hi' (Hindi - auto-generated).
    :return: List of transcript entries.
    """
    # Parse the JSON string into Python objects
    data = json.loads(raw_json_str)

    # If it's not a list or empty, return empty
    if not isinstance(data, list) or len(data) == 0:
        return []

    # Extract tracks from the first item
    item = data[0]
    tracks = item.get("tracks", [])

    # Map the user-friendly language code to the actual "language" field
    language_map = {
        'en': "English",
        'hi': "Hindi (auto-generated)"
    }
    target_language = language_map.get(language, "English")

    # Find the transcript matching the chosen language
    selected_transcript = None
    for track in tracks:
        if track.get("language") == target_language:
            selected_transcript = track.get("transcript", [])
            break

    # If no matching track is found, return empty
    if selected_transcript is None:
        return []

    # Build the output structure
    result = []
    for entry in selected_transcript:
        # 'text' is already a string
        text_str = entry.get("text", "")
        
        # Convert start & duration to floats
        try:
            start_val = float(entry.get("start", 0))
        except ValueError:
            start_val = 0.0
        
        try:
            dur_val = float(entry.get("dur", 0))
        except ValueError:
            dur_val = 0.0
        
        # Create the dictionary
        line_dict = {
            "text": text_str,
            "start": start_val,
            "duration": dur_val
        }
        result.append(line_dict)

    return result


# -----------------------
# Example usage / testing
# -----------------------
if __name__ == "__main__":
    # This is a truncated version of the raw JSON you provided
    raw_json_example = r"""
    [
      {
        "id": "i6bTLmBYNf4",
        "title": "15 Alternatives ...",
        "tracks": [
          {
            "language": "English",
            "transcript": [
              {"text": "Hi guys. I'm Nishant Chahar.", "start": "0", "dur": "0.729"},
              {"text": "And welcome back to the channel. So in today's video were going to talk about",
               "start": "0.73", "dur": "2.278"},
              {"text": "15 such companies whose package is even higher than FAANG company.",
               "start": "3.114", "dur": "4.072"},
              {"text": "Till then - Bye!", "start": "720.786", "dur": "0.762"}
            ]
          },
          {
            "language": "Hindi (auto-generated)",
            "transcript": [
              {"text": "आज की वीडियो में हम बात करने वाले हैं", "start": "0.979", "dur": "4.84"}
            ]
          }
        ]
      }
    ]
    """

    english_subtitles = convert_to_subtitle_dicts(raw_json_example, language='en')
    print("English Subtitles (list of dicts):")
    for line in english_subtitles:
        print(line)

    print("\nHindi Subtitles (list of dicts):")
    hindi_subtitles = convert_to_subtitle_dicts(raw_json_example, language='hi')
    for line in hindi_subtitles:
        print(line)
