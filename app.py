# app.py
from flask import Flask, request, jsonify
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

app = Flask(__name__)
CORS(app)  # allow frontend JS to access backend

@app.route("/story", methods=["POST"])
def story():
    """Generate a short story based on user prompt"""
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    try:
        response = client.chat.completions.create(
            model="mistral-small",  # <-- change here if you want another Mistral model
            messages=[
                {"role": "system", "content": "You are a creative storyteller. Keep stories short and fun."},
                {"role": "user", "content": f"Write a story about: {prompt}"}
            ],
            stream=False
        )

        story_text = response.choices[0].message.content
        return jsonify({"story": story_text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)
