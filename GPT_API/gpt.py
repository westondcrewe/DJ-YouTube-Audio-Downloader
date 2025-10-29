from openai import OpenAI
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_playlist_from_image(image_path):
    # open image and query GPT model
    with open(image_path, "rb") as f:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # vision model
            messages=[
                {"role": "system", "content": "You are an assistant that extracts playlists from screenshots."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract songs and artists as JSON."},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + f.read().encode("base64")}}
                ]}
            ]
        )
    # format json output
    return json.loads(response.choices[0].message["content"])