# Matchmaking Python Email Script/Bot

This is a multi-phase python matchmaking system that generates, evaluates, and notifies users of potential romantic matches based on shared preferences and mutual interest.

## 📁 Project Structure

```
christian-matchmaking/
├── .env
├── email_utils.py
├── phase1.py
├── phase2.py
├── phase2_send.py
├── phase3.py
├── phase3_send.py
├── test2.py
├── test2_send.py
├── test3.py
├── test3_send.py
├── README.md
└── data/
    ├── users.json - paste form data here for phase 1
    ├── phase1_matches.json - generated
    ├── phase2_template.json - you update this 
    ├── phase2_emails.json - generated
    ├── submissions.json - paste form data here for phase 2
    ├── phase3_matches.json - generated
    ├── phase3_emails.json - generated
    └── phase3_template.json - you update this 
```

## ⚙️ Setup Instructions

### 1. Install Python Dependencies

Only `python-dotenv` is needed:

```bash
pip install python-dotenv
```

If pip is unavailable, you can use the lightweight `dotenv.py` alternative included.

---

### 2. Create a `.env` File

Create a `.env` file in the project root with your credentials:

```
EMAIL_ADDRESS=christianmatchmakingbot@gmail.com
EMAIL_PASSWORD=your-app-password-here
DATA_DIR=data/<current-form-identifier-here>
```
---

## 🚀 Running the Pipeline

### Phase 1 – Match Calculation

```bash
python phase1.py
```

Generates `phase1_matches.json` from `users.json` based on mutual preferences.

---

### Phase 2 – Email Match Results (Round 1)

```bash
python phase2.py
# !! You should probably test before running any send scripts !!
python phase2_send.py
```

Sends emails using match results from Phase 1.

---

### Phase 3 – Mutual Interest Submissions

```bash
python phase3.py
# !! You should probably test before running any send scripts !!
python phase3_send.py
```

Generates mutual matches based on submitted interest (`submissions.json`) and sends contact emails directly.

---

### Test Mode

Run test email previews:

```bash
python test1.py
python test1_send.py
python test2.py
python test2_send.py
```

The test scripts render 2 random results for human verification. Run this as many times as you want. 

The `send` test scripts send at most only 10 sample emails to the bot email address for safe testing. 
