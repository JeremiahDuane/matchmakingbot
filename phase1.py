from email_utils import read_json, write_json
import os

def parse_preferences(pref_string):
    return set(pref.strip().upper() for pref in pref_string.split(',') if pref.strip())

def matches_preferences(user_a, user_b):
    prefs_a = user_a.get('prefs', {})
    if not (prefs_a.get('ageMin', 0) <= user_b.get('age', 0) <= prefs_a.get('ageMax', 100)):
        return False
    for key in ['maritalStatus', 'hasKids', 'virginalStatus', 'politic', 'exerciseFreq', 'drinkingFreq']:
        pref_values = parse_preferences(prefs_a.get(key, ''))
        if pref_values and user_b.get(key, '').upper() not in pref_values:
            return False
    return True

def find_matches(users):
    matches_output = []
    for user in users:
        if user.get('gender', '').upper() != 'MALE':
            continue  # Only match males to females
        user_matches = []
        for other in users:
            if other['userID'] == user['userID']:
                continue
            if other.get('gender', '').upper() != 'FEMALE':
                continue
            if matches_preferences(user, other) and matches_preferences(other, user):
                user_matches.append(other['userID'])
        matches_output.append({
            'email': user.get('email', 'Unknown'),
            'userID': user['userID'],
            'matchedUserIDs': user_matches
        })
    return matches_output

if __name__ == "__main__":
    users_data = read_json("users.json")
    matched_users = find_matches(users_data)
    write_json("phase1_matches.json", matched_users)
    print("✅ Matching complete. Results saved to phase1_matches.json.")
