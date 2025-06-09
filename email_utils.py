import json
import re
import os
import smtplib
from email.message import EmailMessage
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPRecipientsRefused, SMTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DATA_DIR = os.getenv("DATA_DIR", "data")  # fallback to 'data'

def read_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)

def write_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --- Formatting Utilities ---

def format_value(value):
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, str):
        if value.lower() == "true":
            return "Yes"
        if value.lower() == "false":
            return "No"
        known_fixes = {
            "NOKIDS": "No Kids", "KIDS": "Kids", "NON-VIRGIN": "Non-Virgin",
            "VIRGIN": "Virgin", "NEVER MARRIED": "Never Married", "WIDOWED": "Widowed",
            "DIVORCED": "Divorced", "SINGLE": "Single"
        }
        upper_value = value.upper()
        if upper_value in known_fixes:
            return known_fixes[upper_value]
        value = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', value)
        value = value.replace("_", " ")
        return value.title()
    return value

def prettify_key(key):
    key = key.replace("_", " ")
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', key).replace("  ", " ").capitalize()

# --- Email Sending ---

def send_email(to_address, subject, body, override_to_address=None):
    actual_to = override_to_address if override_to_address else to_address

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = actual_to
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True, None
    except (SMTPAuthenticationError, SMTPConnectError, SMTPRecipientsRefused, SMTPException) as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"

def send_batch_emails(email_objs, limit=None):
    consecutive_failures = 0
    count = 0
    for email_obj in email_objs:
        recipient = email_obj["recipient"]
        subject = email_obj["title"]
        body = email_obj["body"]

        success, error_msg = send_email(
            to_address=recipient,
            subject=subject,
            body=body
        )

        if success:
            print(f"✅ Email sent to {recipient}")
            consecutive_failures = 0
        else:
            print(f"❌ Failed to send email to {recipient}: {error_msg}")
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("🚨 Stopping after 3 consecutive failures.")
                break

        count += 1
        if limit and count >= limit:
            print(f"ℹ️ Sent {count} emails (limit reached)")
            break
