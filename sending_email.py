import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up the email parameters
sender_email = "campusfixusf@gmail.com"
receiver_email = "kautilyaveer24@gmail.com"
subject = "Enter Subject"
body = "Enter Body"

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
