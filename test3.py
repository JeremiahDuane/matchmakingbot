import json
import random

# Load the email data from the Phase 3 email JSON file
with open('phase3_emails.json', 'r') as f:
    emails = json.load(f)

# Separate emails with and without matches
with_matches = [email for email in emails if "no matches" not in email.get("summary", "").lower()]
without_matches = [email for email in emails if "no matches" in email.get("summary", "").lower()]

# Select one random email from each category
email_with_match = random.choice(with_matches) if with_matches else None
email_without_match = random.choice(without_matches) if without_matches else None

# Function to print email in readable format
def print_email(email, label):
    if email:
        print(f"\n--- {label} ---")
        print(f"Recipient: {email.get('recipient', 'N/A')}")
        print(f"Title    : {email.get('title', 'N/A')}")
        print(f"Summary  : {email.get('summary', 'N/A')}")
        print("\nBody:\n")
        print(email.get('body', ''))
        print("\n" + "-" * 60)

# Print both sample emails
print_email(email_with_match, "Email WITH Matches")
print_email(email_without_match, "Email WITHOUT Matches")
