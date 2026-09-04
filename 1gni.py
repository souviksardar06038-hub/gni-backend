# from flask import Flask, request, jsonify
# from google import genai

# app = Flask(__name__)

# # Aapki Gemini client initialization
# client = genai.Client(api_key="AQ.Ab8RN6JvIoPEYkj6FO3KqHyy3o-CiRw7F5LSYp3VNx1nrVoM5g")

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json
#     user_input = data.get("message", "")
    
#     if not user_input:
#         return jsonify({"error": "Message is required"}), 400

#     try:
#         # Gemini model call
#         response = client.models.generate_content(
#             model="gemini-3.6-flash",  # ya jo model aap use kar rahe hain
#             contents=user_input,
#         )
#         return jsonify({"response": response.text})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
                                            # REPLACE THE CODE ABOVE WITH THE CODE BELOW FOR CLOUD HOSTING

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from openai import api_key

app = Flask(__name__)
CORS(app)  # Mobile App & Web Frontend ke access ke liye

# Gemini Client Setup
# API Key environment variable se lega, agar set nahi hai toh fallback key use karega
api_key = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6JvIoPEYkj6FO3KqHyy3o-CiRw7F5LSYp3VNx1...") # Aapki key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", api_key))

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
            model="gemini-3.6-flash",
            contents=user_input,
        )
        return jsonify({"response": response.text})

    except Exception as e:
        if "503" in str(e):
            return jsonify({"error": "Google API busy, please retry in a few seconds."}), 503
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Cloud hosting dynamically PORT assign karti hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)