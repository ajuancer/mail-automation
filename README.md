# Basic scripts for mail managment
## [`no-reply-response.py`](no-reply-response.py)
Automatic response for my fallback email address that replies to any mail not delievered to existing accounts.

## [`temp-mail-deletion.py`](temp-mail-deletion.py)
Deletes incoming mail to an address following the regex `temp+`[`\w`](https://github.com/ziishaned/learn-regex?tab=readme-ov-file#3-shorthand-character-sets)`@yourdomain.com`.

## [`vaccation-response.py`](vaccation-response.py)
Automatic message response to emails received beetween two dates. Script creates a new tag `Responded` so received emails continue `unseen` and at `inbox`.

Needs a `settings.py` file with the following information:
```python
from datetime import datetime

IMAP_SERVER = 'imap.yourserver.com'
SMTP_SERVER = 'smtp.yourserver.com'
EMAIL_ADDRESS = 'your@mailadrees.com'
EMAIL_PASSWORD = 'your-password'
VACATION_START = datetime(2024, 8, 1)
VACATION_END = datetime(2024, 8, 15)
MAIL_BODY = f"Thanks for your email! I'm currently out of the office, " \
             "I'll be back on {VACATION_END.strftime('%B %d, %Y')}. In the meantime, feel free to reach out to someone who is not enjoying the sun as much as I am!\n\n" \
             "Cheers,\n" \
             "~ a bot"
```