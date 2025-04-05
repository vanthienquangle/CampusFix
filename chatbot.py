from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Set your Gemini API key here (paste it directly)
GEMINI_API_KEY = "AIzaSyAo7Hq1-KXPsGi8XsYxJ_TGAUmKtobJhok"

# Or optionally use this with .env:
# from dotenv import load_dotenv
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Generative AI
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return "Flask server is running!"

# Chat with Gemini-Pro
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_message)
        return jsonify({"message": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# 📸 Analyze Image using Gemini-Pro-Vision
@app.route('/image-report', methods=['POST'])
def image_report():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        image_file = request.files['image']
        image = Image.open(image_file.stream)

        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([
            "Describe the issue in this image for a maintenance report.",
            image
        ])

        return jsonify({"description": response.text})

    except Exception as e:
        print("Image analysis error:", e)
        return jsonify({"error": "Failed to analyze image"}), 500

if __name__ == '__main__':
    app.run(port=5000)
