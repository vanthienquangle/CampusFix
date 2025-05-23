from flask import Flask, request, jsonify, session
from flask_cors import CORS
from PIL import Image
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import json
import os
from dotenv import load_dotenv
from io import BytesIO

# Init Flask
app = Flask(__name__)
CORS(app)

# Load contact responsibilities
with open('contacts.json') as f:
    CONTACTS = json.load(f)

# Select the responsible contact based on keywords
def find_contact_by_issue(issue_text):
    issue_lower = issue_text.lower()
    for role, info in CONTACTS.items():
        for keyword in info["keywords"]:
            if keyword in issue_lower:
                return info  # {name, email, keywords}
    return None

# Load environment variables (EMAIL + GEMINI API)
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


REPORTS = []

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/admin-login', methods=['POST'])
def admin_login():
    creds = request.get_json()
    if creds['username'] == 'campusfixusf@gmail.com' and creds['password'] == 'campusfixiswinningthishackathon040525':
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/api/reports')
def get_reports():
    return jsonify(REPORTS)

@app.route('/api/finish/<int:report_id>', methods=['POST'])
def mark_finished(report_id):
    for r in REPORTS:
        if r['id'] == report_id:
            r['finished'] = True
    return jsonify(success=True)

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
# Send email using Gmail SMTP
def send_email():
    # Generate text from the image
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    image = request.files["image"]
    bytes = image.read()
    imgAttach = MIMEImage(bytes, _subtype = "jpg")
    if not image:
        raise ValueError("No image file found in the request.")
    image = Image.open(BytesIO(bytes))
    
    building = request.form["building"]
    room = "" if not request.form["room"].strip() else f", room {request.form["room"]}"

    model = genai.GenerativeModel("gemini-1.5-flash")

    problemMessage = model.generate_content([
        "Describe the issue in this image for a maintenance report from the perspective of a user reporting the issue in the picture for maintainance request. Don't use any placeholders for any values. Don't make it email format, just simple description of the issue. No new line before or after response text.",
        image
    ]).text

    recipient = find_contact_by_issue(problemMessage)

    subject = model.generate_content([
        "Write a subject of the maintainence inquiry email on one single line, don't include any placeholders for any values. No new line before or after response text.",
        image
    ]).text

    # Set up the email parameters
    sender_email = "campusfixusf@gmail.com"
    receiver_email = recipient["email"] # recipient.email
    print(recipient)
    body = f'''
    Dear {recipient["name"]},

    The following problem is recently reported at {building}{room}:

    {problemMessage}

    Please kindly help sort it out as soon as possible. Thank you for your assistance!

    Best regards,
    CampusFix Team
    '''
    # Create the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    message.attach(imgAttach)

    if recipient is None:
        os.alert("No recipient is found for this issue")

    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = sender_email
    smtp_password = "cnki qxnw eqlg iaex"  # For Gmail, use App Password if 2FA is enabled

    try:
        # Connect to the server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)  # Login
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email

        print("Email sent successfully!")
        return "Successfully sent"
    except Exception as e:
        import traceback
        traceback.print_exc()  # 👈 this prints full stack trace to your terminal
        return f"Failed: {str(e)}", 500  # 👈 this sends the error back to your fetch


if __name__ == '__main__':
    app.run(debug=True, port=5000)