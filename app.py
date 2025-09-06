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


# Helper to enforce paragraph + word limits
def enforce_paragraph_constraints(text: str, paragraphs: int = 3, words_per_para: int = 100) -> str:
    # Split by double newlines into paragraphs
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    
    # If too many, trim; if too few, pad with empty
    if len(paras) > paragraphs:
        paras = paras[:paragraphs]
    while len(paras) < paragraphs:
        paras.append("")

    processed = []
    for p in paras:
        words = p.split()
        if len(words) > words_per_para:
            out = " ".join(words[:words_per_para]).rstrip()
            if out and out[-1] not in ".!?":
                out += "..."
            processed.append(out)
        else:
            processed.append(" ".join(words))
    return "\n\n".join(processed)


@app.route("/")
def serve_index():
    """Serve the frontend file"""
    return send_from_directory(".", "index.html")


@app.route("/story", methods=["POST"])
def story():
    """Generate a 3-paragraph story, 100 words per paragraph"""
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    try:
        response = client.chat.completions.create(
            model="mistral-small",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a skilled storyteller. "
                        "Always write stories in exactly 3 paragraphs. "
                        "Each paragraph should be around 100 words, "
                        "and the story must be complete within those 3 paragraphs."
                    )
                },
                {
                    "role": "user",
                    "content": f"Write a complete 3-paragraph story (100 words each) about: {prompt}"
                }
            ],
            max_tokens=600,   # enough room for ~300 words
            temperature=0.9,
            stream=False
        )

        raw_story = response.choices[0].message.content
        story_text = enforce_paragraph_constraints(raw_story, paragraphs=3, words_per_para=100)
        return jsonify({"story": story_text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
