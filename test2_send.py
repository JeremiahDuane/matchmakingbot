import random
from email_utils import read_json, send_batch_emails

emails = read_json("phase2_emails.json")
with_matches = [e for e in emails if "no matches" not in e.get("summary", "").lower()]
without_matches = [e for e in emails if "no matches" in e.get("summary", "").lower()]

samples = []
if with_matches:
    samples.append(random.choice(with_matches))
if without_matches:
    samples.append(random.choice(without_matches))

send_batch_emails(samples)
