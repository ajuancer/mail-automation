import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import os

# Email server configuration
IMAP_SERVER = 'imap.example.com'
SMTP_SERVER = 'smtp.example.com'
EMAIL_ADDRESS = 'no-reply@yourdomain.com'
EMAIL_PASSWORD = 'your-password'

# Function to send automatic response
def send_auto_response(sender_name, sender_email, original_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = sender_email
    msg['Subject'] = 'Email Address Not Found'

    body = f"Hi {sender_name},\n\nThis is an automatic response to let you know that the email address \"{original_email}\" does not exist, so your message wasn't delivered to anyone. It might be a typo. Take care!\n\nBest regards,\n a bot"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, sender_email, msg.as_string())
    server.quit()


# Connect to the email server and check for new emails
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
mail.select('inbox')

status, response = mail.search(None, 'UNSEEN')
email_ids = response[0].split()

for email_id in email_ids:
    status, response = mail.fetch(email_id, '(RFC822)')
    msg = email.message_from_bytes(response[0][1])

    sender_email = email.utils.parseaddr(msg['From'])[1]
    sender_name = email.utils.parseaddr(msg['From'])[0]

    original_email = EMAIL_ADDRESS
    send_auto_response(sender_name, sender_email, original_email)

    mail.store(email_id, '+FLAGS', '\\Seen')

mail.logout()
