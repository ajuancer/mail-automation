import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from datetime import datetime
from datetime import timedelta
from settings import EMAIL_ADDRESS, EMAIL_PASSWORD, MAIL_BODY, SMTP_SERVER, IMAP_SERVER, VACATION_END, VACATION_START



# Function to send vacation response
def send_vacation_response(sender_name, sender_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = sender_email
    msg['Subject'] = 'Out of Office: On Vacation!'

    body = (
        f"Hi {sender_name},\n\n"+ MAIL_BODY
    )
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, sender_email, msg.as_string())
    server.quit()


mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
mail.select('inbox')


search_criteria = (
    f'(SINCE "{VACATION_START.strftime("%d-%b-%Y")}" BEFORE "{(VACATION_END + timedelta(days=1)).strftime("%d-%b-%Y")}")'
)
status, response = mail.search(None, search_criteria)
email_ids = response[0].split()

RESPONDED_LABEL = 'Responded'

for email_id in email_ids:
    status, response = mail.fetch(email_id, '(RFC822)')
    msg = email.message_from_bytes(response[0][1])

    sender_email = email.utils.parseaddr(msg['From'])[1]
    sender_name = email.utils.parseaddr(msg['From'])[0]

    status, response = mail.fetch(email_id, '(X-GM-LABELS)')
    labels = email.message_from_bytes(response[0][1]).get('X-GM-LABELS', '')

    if RESPONDED_LABEL not in labels:
        send_vacation_response(sender_name, sender_email)
        mail.store(email_id, '+X-GM-LABELS', RESPONDED_LABEL)

mail.logout()
