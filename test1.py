import json
import random

# Load users and matches data
with open('users.json', 'r') as f:
    users = json.load(f)

with open('phase1_matches.json', 'r') as f:
    matches = json.load(f)

user_dict = {user['userID']: user for user in users}
eligible_users = [entry for entry in matches if entry['matchedUserIDs']]
selected_entry = random.choice(eligible_users)
selected_user = next(user for user in users if user['email'] == selected_entry['email'])
selected_user_id = selected_user['userID']

matched_user_id = random.choice(selected_entry['matchedUserIDs'])
matched_user = user_dict[matched_user_id]

filtered_keys = ['age', 'maritalStatus', 'hasKids', 'virginalStatus', 'politic', 'exerciseFreq', 'drinkingFreq']

# Table 1: Selected user's values vs matched user's preferences
print(f"\nUser {selected_user_id} Values vs Preferences of Matched User {matched_user_id}")
print(f"{'Attribute':<25} | {'User Value':<20} | {'Matched User Preference':<30}")
print("-" * 80)
for key in filtered_keys:
    user_val = str(selected_user.get(key, 'N/A'))
    if key == 'age':
        match_pref = f"{matched_user.get('prefs', {}).get('ageMin', 'N/A')} - {matched_user.get('prefs', {}).get('ageMax', 'N/A')}"
    else:
        match_pref = str(matched_user.get('prefs', {}).get(key, 'N/A'))
    print(f"{key:<25} | {user_val:<20} | {match_pref:<30}")

# Table 2: Matched user's values vs selected user's preferences
print(f"\nMatched User {matched_user_id} Values vs Preferences of User {selected_user_id}")
print(f"{'Attribute':<25} | {'Matched User Value':<20} | {'User Preference':<30}")
print("-" * 80)
for key in filtered_keys:
    match_val = str(matched_user.get(key, 'N/A'))
    if key == 'age':
        user_pref = f"{selected_user.get('prefs', {}).get('ageMin', 'N/A')} - {selected_user.get('prefs', {}).get('ageMax', 'N/A')}"
    else:
        user_pref = str(selected_user.get('prefs', {}).get(key, 'N/A'))
    print(f"{key:<25} | {match_val:<20} | {user_pref:<30}")