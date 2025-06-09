from email_utils import read_json, send_batch_emails

emails = read_json("phase3_emails.json")
send_batch_emails(emails)