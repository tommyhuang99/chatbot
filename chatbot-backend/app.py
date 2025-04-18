from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Use environment variable for API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Validate request JSON
        if not request.json or "message" not in request.json:
            return jsonify({"error": "Invalid request"}), 400

        user_message = request.json["message"]

        # Call OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            # Validate response structure
            bot_reply = response.choices[0].message.content
        except Exception as api_error:
            return jsonify({"error": f"OpenAI API error: {str(api_error)}"}), 500

        # Return bot's reply
        return jsonify({"reply": bot_reply})

    except Exception as e:
        # Handle general errors
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
