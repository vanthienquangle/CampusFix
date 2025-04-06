import google.generativeai as genai
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Generate text from the image
genai.configure(api_key="AIzaSyDQa8b4K1Wcpc3OhpXBtGDgym5eXJgtPOY")

image = Image.open("image.jpg")

model = genai.GenerativeModel("gemini-1.5-flash")

problemMessage = model.generate_content([
    "Describe the problem identified in the provided image",
    image
]).text

subject = mode.generate_content([
    "We are writing an email to the maintainance team for the problem in the image. Create an email subject about it with the structure: 'Inquiry of (problem)'",
    image
])

# Set up the email parameters
sender_email = "campusfixusf@gmail.com"
receiver_email = "kautilyaveer24@gmail.com"
body = f'''
Dear (receiver),

The following problem is recently reported at (building), room (room):
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
except Exception as e:
    print(f"Error: {e}")
