MoodJournal (AI Semester Project): 

MoodJournal is an AI-powered mood tracking journal built with Streamlit. It allows you to write daily entries, automatically detects your mood using advanced keyword and sentiment analysis, and provides motivational quotes and analytics.

Features:

Write and save daily journal entries
Automatic mood detection (supports 10+ moods)
Mood scoring and visualization
Motivational quotes based on your mood
Analytics dashboard for mood trends and distribution
Search, filter, edit, and delete entries


Installation:
Install Python dependencies:
pip install -r requirements.txt



(First time only) Download NLTK resources
The app will attempt to download required NLTK data automatically. If you see errors, run:
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')



Prepare data files:

Make sure mood_keywords.json is present in the project directory.
The app will create journal_entries.csv automatically when you save your first entry.


Usage:
Start the app:
streamlit run app.py


Open your browser:
Visit the local URL shown in your terminal (usually http://localhost:8501).


Write your journal entry:

Go to the "✏️ Journal" tab.
Enter the date, title, and your thoughts.
The app will analyze your mood and display a motivational quote.



View analytics:
Go to the "📊 Analytics" tab to see your mood trends and statistics.



Manage entries:
Use the "📝 Entries" tab to search, filter, edit, or delete your journal entries.


File Structure:

app.py — Main Streamlit app
mood_analyzer.py — Mood detection logic (keyword and sentiment analysis)
data_manager.py — Handles saving/loading journal entries
visualization.py — Analytics and plotting functions
mood_keywords.json — List of moods and associated keywords (required)
journal_entries.csv — Your saved journal entries (auto-created)
requirements.txt — Python dependencies


Notes:

Standard library modules (os, re, uuid, etc.) are used and do not require installation.
All data is stored locally in CSV and JSON files.
For best results, ensure your mood_keywords.json contains at least 10 moods and 200+ keywords.


TroubleshootingL:

If you see errors about missing NLTK data, run the download commands in a Python shell.
If you change the structure of the JSON files, make sure the keys and formats match the code expectations.


Enjoy tracking your mood and journaling your thoughts!
