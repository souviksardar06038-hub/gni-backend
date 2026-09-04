import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Gemini Client Setup (API key environment variable se lega)
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Server is running successfully!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
        )
        return jsonify({"response": response.text})

    except Exception as e:
        if "503" in str(e):
            return jsonify({"error": "Google API busy, please retry in a few seconds."}), 503
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)