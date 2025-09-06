from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load .env file
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise RuntimeError("No MISTRAL_API_KEY found in .env file!")

# Initialize OpenAI-compatible client with Mistral base URL
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.mistral.ai/v1"
)

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)  # allow frontend JS to access backend

# Helper function to enforce word limit
def truncate_to_n_words(text: str, n: int = 100) -> str:
    words = text.split()
    if len(words) <= n:
        return text.strip()
    out = " ".join(words[:n]).rstrip()
    if out and out[-1] not in ".!?":
        out += "..."
    return out

@app.route("/")
def serve_index():
    """Serve the frontend file"""
    return send_from_directory(".", "index.html")

@app.route("/story", methods=["POST"])
def story():
    """Generate a short story based on user prompt (limited to 100 words)"""
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    try:
        response = client.chat.completions.create(
            model="mistral-small",  # change if you want another Mistral model
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative storyteller. Keep stories short (~100 words), fun, and self-contained."
                },
                {
                    "role": "user",
                    "content": f"Write a story in about 100 words about: {prompt}"
                }
            ],
            max_tokens=180,   # gives space for ~100 words
            temperature=0.9,
            stream=False
        )

        raw_story = response.choices[0].message.content
        story_text = truncate_to_n_words(raw_story, 100)   # enforce hard cap
        return jsonify({"story": story_text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
