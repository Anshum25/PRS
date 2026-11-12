# 🚀 Post Recommendation System for @TheAnshumDev

A tailored content engine and trend assistant built specifically for [@TheAnshumDev](https://x.com/TheAnshumDev).

## ✨ What This Does
1. **Scans Live Tech & AI Trends**: Pulls real-time discussions from Hacker News, Reddit (`r/MachineLearning`, `r/ProgrammerHumor`), and Google Tech News.
2. **Applies Your Exact Persona**: Formats posts to match your grounded, anti-hype, mathematical, self-aware developer voice (no cringe marketing cliches or emoji spam).
3. **Generates 4 Targeted Formats**:
   - **Option 1: The Witty Anti-Hype Take** (Viral / High Retweets)
   - **Option 2: The Systems / ML Practitioner Angle** (High Bookmarks)
   - **Option 3: The Honest Learner Grind & Quiet Discipline** (Authenticity / Trust)
   - **Option 4: The Provocative Discussion Question** (High Replies & Engagement)
4. **Auto-saves to `drafts.md`**: Easily review and copy-paste directly to X.

---

## 🛠️ How to Run

### Step 1: Open the directory
```bash
cd post_recommendation_system
```

### Step 2: Set your Gemini API Key
Create a `.env` file or simply run the script (it will prompt you if not set):
```bash
cp .env.example .env
# Edit .env and paste your free Gemini API key from https://aistudio.google.com/app/apikey
```

### Step 3: Run the interactive CLI
```bash
python3 main.py
```

### Step 4: Pick your draft & post!
Open `drafts.md` or copy directly from the terminal, make any final tweaks, and post on X.
