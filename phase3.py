from email_utils import read_json, write_json, format_value, prettify_key

users = read_json("users.json")
submissions = read_json("submissions.json")
template = read_json("phase3_template.json")

email_to_userid = {u["email"]: u["userID"] for u in users}
user_dict = {u["userID"]: u for u in users}

user_wants = {}
user_email = {}

for entry in submissions:
    email = entry["username"]
    user_id = email_to_userid.get(email)
    if user_id:
        user_wants[user_id] = entry["wants"]
        user_email[user_id] = email

matches = []

for user_id, wants in user_wants.items():
    mutuals = [tid for tid in wants if tid in user_wants and user_id in user_wants[tid]]
    matches.append({
        "email": user_email[user_id],
        "userID": user_id,
        "matchedUserIDs": mutuals
    })

write_json("phase3_matches.json", matches)
print("✅ phase3_matches.json saved.")

emails = []

for match_entry in matches:
    email = match_entry["email"]
    matched_ids = match_entry["matchedUserIDs"]

    if not matched_ids:
        body = f"Recipient Email: {email}\n\n{template['no_matches_message']}\n\n{template['signature']}"
        summary = "No matches this time"
    else:
        summary = "You have new matches!"
        body_lines = [f"Recipient Email: {email}", "", template["matches_message"], ""]
        for mid in matched_ids:
            match = user_dict.get(mid, {})
            body_lines.append(f"Match ID: {mid}")
            for key, value in match.items():
                if key in ['prefs', 'email', 'userID', 'timestamp', 'virginalStatus']:
                    continue
                body_lines.append(f"  {prettify_key(key)}: {format_value(value)}")
            body_lines.append("")
        body_lines.append("Contact your matches directly using their email addresses:")
        for mid in matched_ids:
            body_lines.append(f"  • {user_dict[mid]['email']}")
        body_lines.append("")
        body_lines.append(template['signature'])
        body = "\n".join(body_lines)

    emails.append({
        "recipient": email,
        "title": "Your Match Results",
        "summary": summary,
        "body": body
    })

write_json("phase3_emails.json", emails)
print("✅ phase3_emails.json saved.")
