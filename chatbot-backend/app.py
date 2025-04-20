from multiprocessing import Semaphore
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from gpt4all import GPT4All

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load GPT4All model once at startup
MODEL_PATH = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = None

try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    model = GPT4All(MODEL_PATH)
except Exception as e:
    print(f"Failed to load GPT4All model: {e}")

@app.route("/health", methods=["GET"])
def health():
    if model is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not request.is_json or "message" not in request.json:
            return jsonify({"error": "Invalid request"}), 400

        user_message = request.json["message"]

        # Use GPT4All model to generate a reply
        with model.chat_session():
            bot_reply = model.generate(user_message, max_tokens=1024)

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
