from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from gpt4all import GPT4All
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Model configuration
# Use a model that comes with gpt4all by default
# This is a smaller model that should be downloadable
MODEL_NAME = "orca-mini-3b-gguf2-q4_0"
model = None
max_retries = 3


def load_model():
    """Load the GPT4All model with retries and auto-download if needed"""
    global model

    for attempt in range(max_retries):
        try:
            print(
                f"Attempt {attempt+1}/{max_retries} to load model {MODEL_NAME}...")
            # GPT4All will automatically download the model if it's not found
            model = GPT4All(model_name=MODEL_NAME)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Failed to load model (attempt {attempt+1}): {str(e)}")
            if attempt < max_retries - 1:
                print("Waiting before retry...")
                time.sleep(2)  # Wait before retrying

    return False


# Try to load the model at startup
try:
    load_model()
except Exception as e:
    print(f"Error during initial model loading: {str(e)}")


@app.route("/health", methods=["GET"])
def health():
    if model is None:
        # Try to load the model if it's not loaded yet
        try:
            if load_model():
                return jsonify({"status": "ok"})
            else:
                return jsonify({"status": "error", "message": "Failed to load model after multiple attempts"}), 500
        except Exception as e:
            return jsonify({"status": "error", "message": f"Error loading model: {str(e)}"}), 500
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Check if model is loaded, try to load it if not
        if model is None:
            if not load_model():
                return jsonify({"error": "Model could not be loaded"}), 500

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
