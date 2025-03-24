from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Thiết lập API Key của Google Cloud
genai.configure(api_key="AIzaSyBRjAIpyMH7EJsKuX855o3qqf1lV3AUUs8")  # Thay YOUR_GOOGLE_CLOUD_API_KEY bằng API Key của bạn

# Route cho trang chủ
@app.route('/')
def home():
    return "Flask server is running!"

# Route cho chatbot
@app.route('/chat', methods=['POST'])
def chat():
    # Lấy tin nhắn từ frontend
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Gọi API Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_message)

        # Trả về phản hồi từ chatbot
        bot_message = response.text
        return jsonify({"message": bot_message})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == '__main__':
    app.run(port=5000)  # Chạy server trên cổng 5000