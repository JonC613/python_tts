import json
import os
import re
from gtts import gTTS
from pathlib import Path

# Create necessary directories if they don't exist
data_dir = Path("data")
mp3_dir = Path("mp3")
data_dir.mkdir(exist_ok=True)
mp3_dir.mkdir(exist_ok=True)

def sanitize_filename(filename):
    print(f"Sanitizing filename: '{filename}'")
    # Remove invalid characters and replace spaces with underscores
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    cleaned = cleaned.replace(' ', '_').lower()
    print(f"Sanitized result: '{cleaned}'")
    return cleaned

def generate_audio_files():
    # Read the JSON file
    try:
        json_path = data_dir / "sight_words.json"
        print(f"Reading JSON file from: {json_path}")
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"Loaded JSON structure: {type(data)}")
            print(f"JSON content preview: {str(data)[:100]}...")
            
        # Check if words is a list, if not, convert to list
        if isinstance(data, dict):
            print("Converting dictionary to list...")
            if 'sight_words' in data:
                words = data['sight_words']
            else:
                words = list(data.values())
            print(f"Extracted {len(words)} words from dictionary")
        elif isinstance(data, list):
            words = data
            print(f"Found list with {len(words)} words")
        else:
            raise ValueError(f"Unexpected JSON content type: {type(data)}")
            
        # Generate audio file for each word
        for word in words:
            word = str(word).strip()
            if not word:
                print("Skipping empty word")
                continue
                
            # Create sanitized filename
            safe_filename = sanitize_filename(word)
            audio_file = mp3_dir / f"{safe_filename}.mp3"
            print(f"\nProcessing word: '{word}'")
            print(f"Target audio file: {audio_file}")
            
            # Skip if file already exists
            if audio_file.exists():
                print(f"Skipping existing file: {audio_file}")
                continue
                
            print(f"Generating audio for: '{word}'")
            try:
                tts = gTTS(text=word, lang='en', slow=False)
                tts.save(str(audio_file))
                print(f"Successfully saved audio for: '{word}'")
            except Exception as e:
                print(f"Error generating audio for '{word}': {str(e)}")
            
        print("\nAudio generation complete!")
            
    except FileNotFoundError:
        print(f"Error: Could not find file at {json_path}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_path}")
        print(f"JSON error details: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    generate_audio_files()