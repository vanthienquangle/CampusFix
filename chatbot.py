from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from dotenv import load_dotenv

# Load environment variables (EMAIL + GEMINI API)
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load contact responsibilities
with open('contacts.json') as f:
    CONTACTS = json.load(f)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Init Flask
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Flask server is running!"

# Chat with Gemini
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_message)
        return jsonify({"message": response.text})
    except Exception as e:
        print(f"Chat Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Analyze image and describe the issue
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

# AI writes + sends email to proper contact
@app.route('/email-with-ai', methods=['POST'])
def email_with_ai():
    data = request.get_json()
    raw_issue = data.get("issue", "")
    location = data.get("location", "Unknown Area")

    if not raw_issue:
        return jsonify({"error": "Missing issue"}), 400

    try:
        # AI writes the message
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Write a professional maintenance request email based on the following report:
Location: {location}
Issue: {raw_issue}
Make sure it's polite and clear."""
        response = model.generate_content(prompt)
        email_body = response.text

        # Auto-select the recipient
        contact = find_contact_by_issue(raw_issue)
        if not contact:
            return jsonify({"error": "No responsible individual found"}), 400

        subject = f"Campus Maintenance Issue - {location}"
        if send_email(subject, email_body, recipient=contact["email"]):
            return jsonify({
                "status": "Email sent successfully",
                "email_body": email_body,
                "recipient": contact["name"]
            })
        else:
            return jsonify({"error": "Failed to send email"}), 500

    except Exception as e:
        print("AI Email Generation Error:", e)
        return jsonify({"error": "Failed to generate or send email"}), 500

# Select the responsible contact based on keywords
def find_contact_by_issue(issue_text):
    issue_lower = issue_text.lower()
    for role, info in CONTACTS.items():
        for keyword in info["keywords"]:
            if keyword in issue_lower:
                return info  # {name, email, keywords}
    return None

# Send email using Gmail SMTP
def send_email(subject, body, recipient):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False

if __name__ == '__main__':
    app.run(port=5000)