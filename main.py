from flask import Flask, jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)

# Load SMTP server and email credentials from the configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

SMTP_SERVER = config['SMTP_SERVER']
SMTP_PORT = config['SMTP_PORT']
SMTP_USERNAME = config['SMTP_USERNAME']
SMTP_PASSWORD = config['SMTP_PASSWORD']
SENDER_EMAIL = config['SENDER_EMAIL']
CC_EMAIL = config.get('CC_EMAIL', '')

def send_email(subject, content, recipient_email):
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(content, 'html'))
    msg['Subject'] = subject
    msg['To'] = recipient_email
    if CC_EMAIL:
        msg['Cc'] = CC_EMAIL

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            recipients = [recipient_email]
            if CC_EMAIL:
                recipients.append(CC_EMAIL)
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        print(f"Sent email to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {str(e)}")

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    action = data.get('action')
    email = data.get('email')
    subject = f"Task {action.capitalize()}"
    message = f"The task '{data.get('task')}' has been {action}."
    
    send_email(subject, message, email)
    return jsonify({'message': 'Notification sent!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
