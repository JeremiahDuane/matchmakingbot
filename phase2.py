from email_utils import read_json, write_json, format_value, prettify_key

users = read_json("users.json")
matches = read_json("phase1_matches.json")
template = read_json("phase2_template.json")

user_dict = {user["userID"]: user for user in users}
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
        body_lines.append(f"Respond here: {template['response_link']}")
        body_lines.append("")
        body_lines.append(template['signature'])
        body = "\n".join(body_lines)

    emails.append({
        "recipient": email,
        "title": "Your Match Results",
        "summary": summary,
        "body": body
    })

write_json("phase2_emails.json", emails)
print("✅ phase2_emails.json saved.")
