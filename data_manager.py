import pandas as pd
import os
import uuid
from datetime import datetime

# Path to the journal entries CSV file
DATA_FILE = "journal_entries.csv"

def load_journal_entries():
    """
    Load all journal entries from the CSV file.
    
    Returns:
        pandas.DataFrame: A DataFrame containing all journal entries.
    """
    if os.path.exists(DATA_FILE):
        try:
            entries = pd.read_csv(DATA_FILE)
            return entries
        except Exception as e:
            print(f"Error loading journal entries: {e}")
            return pd.DataFrame(columns=['id', 'date', 'title', 'content', 'mood', 'mood_score'])
    else:
        # Create a new DataFrame if the file doesn't exist
        return pd.DataFrame(columns=['id', 'date', 'title', 'content', 'mood', 'mood_score'])

def save_journal_entry(date, title, content, mood, mood_score):
    """
    Save a new journal entry to the CSV file.
    
    Args:
        date (str): The date of the entry in YYYY-MM-DD format.
        title (str): The title of the entry.
        content (str): The content of the entry.
        mood (str): The mood analyzed from the entry.
        mood_score (float): The mood score from the sentiment analysis.
        
    Returns:
        bool: True if the entry was saved successfully, False otherwise.
    """
    try:
        # Load existing entries
        entries = load_journal_entries()
        
        # Create a new entry
        new_entry = pd.DataFrame({
            'id': [str(uuid.uuid4())],
            'date': [date],
            'title': [title],
            'content': [content],
            'mood': [mood],
            'mood_score': [mood_score]
        })
        
        # Append the new entry
        entries = pd.concat([entries, new_entry], ignore_index=True)
        
        # Save the updated entries to the CSV file
        entries.to_csv(DATA_FILE, index=False)
        
        return True
    except Exception as e:
        print(f"Error saving journal entry: {e}")
        return False

def update_journal_entry(entry_id, date, title, content, mood, mood_score):
    """
    Update an existing journal entry.
    
    Args:
        entry_id (str): The ID of the entry to update.
        date (str): The updated date of the entry.
        title (str): The updated title of the entry.
        content (str): The updated content of the entry.
        mood (str): The updated mood analyzed from the entry.
        mood_score (float): The updated mood score.
        
    Returns:
        bool: True if the entry was updated successfully, False otherwise.
    """
    try:
        # Load existing entries
        entries = load_journal_entries()
        
        # Find the entry with the given ID
        entry_index = entries[entries['id'] == entry_id].index
        
        if len(entry_index) > 0:
            # Update the entry
            entries.loc[entry_index, 'date'] = date
            entries.loc[entry_index, 'title'] = title
            entries.loc[entry_index, 'content'] = content
            entries.loc[entry_index, 'mood'] = mood
            entries.loc[entry_index, 'mood_score'] = mood_score
            
            # Save the updated entries to the CSV file
            entries.to_csv(DATA_FILE, index=False)
            
            return True
        else:
            print(f"Entry with ID {entry_id} not found.")
            return False
    except Exception as e:
        print(f"Error updating journal entry: {e}")
        return False

def delete_journal_entry(entry_id):
    """
    Delete a journal entry.
    
    Args:
        entry_id (str): The ID of the entry to delete.
        
    Returns:
        bool: True if the entry was deleted successfully, False otherwise.
    """
    try:
        # Load existing entries
        entries = load_journal_entries()
        
        # Check if the entry exists
        if entry_id not in entries['id'].values:
            print(f"Entry with ID {entry_id} not found.")
            return False
        
        # Remove the entry
        entries = entries[entries['id'] != entry_id]
        
        # Save the updated entries to the CSV file
        entries.to_csv(DATA_FILE, index=False)
        
        return True
    except Exception as e:
        print(f"Error deleting journal entry: {e}")
        return False