import imaplib
import email
from email.header import decode_header
import datetime
import re

IMAP_SERVER = 'imap.your-email-provider.com'
EMAIL_ACCOUNT = 'temp+[random set of chars]@juancer.me'
PASSWORD = 'yourpassword'

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, PASSWORD)

mail.select("inbox")

result, data = mail.search(None, "ALL")

email_ids = data[0].split()

date_15_days_ago = (datetime.datetime.now() -
                    datetime.timedelta(days=15)).strftime("%d-%b-%Y")

email_pattern = re.compile(r"temp\+\w+@yourdomain\.com")

for email_id in email_ids:
    result, msg_data = mail.fetch(email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    email_date = email.utils.parsedate_to_datetime(msg["Date"])

    if email_date < datetime.datetime.strptime(date_15_days_ago, "%d-%b-%Y"):
        to_address = msg.get("To")
        if email_pattern.match(to_address):
            mail.store(email_id, "+FLAGS", "\\Deleted")

mail.expunge()

mail.logout()
