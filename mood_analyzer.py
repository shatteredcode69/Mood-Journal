import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import json
import os

# Download necessary NLTK resources
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')
    nltk.download('punkt')

# Load mood keywords and quotes
def load_mood_data():
    """Load mood keywords and quotes from JSON file."""
    try:
        with open('mood_keywords.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: mood_keywords.json not found")
        return None

def analyze_mood(text):
    """
    Analyze the mood of a text entry using keyword matching and sentiment analysis.
    
    Args:
        text (str): The journal entry text to analyze.
        
    Returns:
        tuple: (mood_label, mood_score, quote) where mood_label is a string label,
               mood_score is a float between -1 and 1, and quote is a motivational quote.
    """
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Clean the text
    clean_text = clean_text_for_analysis(text)
    
    # Get sentiment scores
    sentiment = sia.polarity_scores(clean_text)
    mood_score = sentiment['compound']
    
    # Load mood data
    mood_data = load_mood_data()
    if not mood_data:
        return "Neutral", mood_score, "Error loading mood data"
    
    # Initialize mood scores
    mood_scores = {mood: 0 for mood in mood_data['moods'].keys()}
    
    # Count keyword matches for each mood
    for mood, data in mood_data['moods'].items():
        for keyword in data['keywords']:
            matches = len(re.findall(r'\b' + keyword + r'\b', clean_text, re.IGNORECASE))
            mood_scores[mood] += matches
    
    # Get the mood with the highest score
    max_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
    
    # If no keywords matched, use sentiment analysis
    if mood_scores[max_mood] == 0:
        if mood_score >= 0.5:
            max_mood = "Joyful"
        elif mood_score >= 0.1:
            max_mood = "Peaceful"
        elif mood_score <= -0.5:
            max_mood = "Sad"
        elif mood_score <= -0.1:
            max_mood = "Anxious"
        else:
            max_mood = "Neutral"
    
    # Get the quote for the detected mood
    quote = mood_data['moods'][max_mood]['quote']
    
    return max_mood, mood_score, quote

def clean_text_for_analysis(text):
    """
    Clean and prepare text for sentiment analysis.
    
    Args:
        text (str): The raw text to clean.
        
    Returns:
        str: Cleaned text ready for analysis.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text