import streamlit as st
import pandas as pd
from datetime import datetime
import time

from mood_analyzer import analyze_mood
from data_manager import load_journal_entries, save_journal_entry, delete_journal_entry, update_journal_entry
from visualization import plot_mood_history, plot_mood_distribution

# Set page configuration
st.set_page_config(
    page_title="MoodJournal - AI-Powered Mood Tracking",
    page_icon="📔",
    layout="wide"
)

# App title and description
st.title("📔 MoodJournal")
st.subheader("AI-Powered Mood Tracking Journal")

# Initialize session state variables
if 'entries' not in st.session_state:
    st.session_state.entries = load_journal_entries()
if 'current_entry_id' not in st.session_state:
    st.session_state.current_entry_id = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'filter_mood' not in st.session_state:
    st.session_state.filter_mood = "All"

# Function to reset the current entry
def reset_entry():
    st.session_state.current_entry_id = None
    st.session_state.edit_mode = False

# Main layout with tabs
tab1, tab2, tab3 = st.tabs(["✏️ Journal", "📊 Analytics", "📝 Entries"])

# Tab 1: Journal Entry
with tab1:
    col1, col2 = st.columns([7, 3])
    
    with col1:
        st.header("Today's Entry" if not st.session_state.edit_mode else "Edit Entry")
        
        # Date selection and input fields
        date = st.date_input(
            "Date",
            value=datetime.now().date() if not st.session_state.edit_mode else 
                  pd.to_datetime(st.session_state.entries[
                      st.session_state.entries['id'] == st.session_state.current_entry_id
                  ]['date'].values[0]).date() if st.session_state.current_entry_id else datetime.now().date()
        )
        
        title = st.text_input(
            "Title",
            value="" if not st.session_state.edit_mode else 
                  st.session_state.entries[
                      st.session_state.entries['id'] == st.session_state.current_entry_id
                  ]['title'].values[0] if st.session_state.current_entry_id else ""
        )
        
        content = st.text_area(
            "Journal Entry",
            height=300,
            value="" if not st.session_state.edit_mode else 
                  st.session_state.entries[
                      st.session_state.entries['id'] == st.session_state.current_entry_id
                  ]['content'].values[0] if st.session_state.current_entry_id else ""
        )
        
        if st.button("Save Entry", key="save_button"):
            if not title or not content:
                st.error("Please provide both a title and content for your journal entry.")
            else:
                # Analyze the mood of the entry
                mood, mood_score, quote = analyze_mood(content)

                
                # Save the entry
                if st.session_state.edit_mode and st.session_state.current_entry_id:
                    update_journal_entry(
                        st.session_state.current_entry_id,
                        date.strftime("%Y-%m-%d"),
                        title,
                        content,
                        mood,
                        mood_score
                    )
                    st.success(f"Journal entry updated successfully! Detected mood: {mood}")
                else:
                    save_journal_entry(
                        date.strftime("%Y-%m-%d"),
                        title,
                        content,
                        mood,
                        mood_score
                    )
                    st.success(f"Journal entry saved successfully! Detected mood: {mood}")
                
                # Reload the journal entries
                st.session_state.entries = load_journal_entries()
                
                # Reset edit mode and current entry
                reset_entry()
                time.sleep(2)
                st.rerun()
        
        if st.session_state.edit_mode:
            if st.button("Cancel Editing", key="cancel_button"):
                reset_entry()
                st.rerun()
    
    with col2:
        st.header("Your Mood")
        if content:
            mood, mood_score, quote = analyze_mood(content)
            
            # Display the detected mood
            mood_emoji = {
                "Joyful": "😊",
                "Peaceful": "😌",
                "Energetic": "⚡",
                "Creative": "🎨",
                "Neutral": "😐",
                "Reflective": "🤔",
                "Anxious": "😰",
                "Sad": "😢",
                "Angry": "😠",
                "Confused": "😕"
            }
            
            st.markdown(f"### {mood_emoji.get(mood, '😐')} {mood}")
            
            # Display mood score
            st.progress(
                (mood_score + 1) / 2,  # Convert from [-1, 1] to [0, 1]
                text=f"Mood Score: {mood_score:.2f}"
            )
            
            # Display motivational quote
            st.markdown("### Motivational Quote")
            st.info(quote)
            
            # Tips based on mood
            st.markdown("### Tips")
            if mood == "Joyful":
                st.info("Great mood! Consider journaling about what made you happy today to remember it in the future.")
            elif mood == "Peaceful":
                st.info("Your peaceful state is valuable. Consider practicing mindfulness to maintain this balance.")
            elif mood == "Energetic":
                st.info("Channel your energy into productive activities or creative pursuits.")
            elif mood == "Creative":
                st.info("Your creative energy is flowing! Consider starting a new project or exploring new ideas.")
            elif mood == "Reflective":
                st.info("Your reflective state is perfect for personal growth. Consider setting new goals or intentions.")
            elif mood == "Anxious":
                st.info("Practice deep breathing exercises or try the 5-4-3-2-1 grounding technique to reduce anxiety.")
            elif mood == "Sad":
                st.info("Take a deep breath. Consider doing something you enjoy or reach out to a friend.")
            elif mood == "Angry":
                st.info("Try taking a short walk or practice deep breathing to calm down.")
            elif mood == "Confused":
                st.info("It's okay to feel uncertain. Take time to reflect and break down your thoughts into smaller pieces.")
            else:
                st.info("Keep journaling regularly to track changes in your mood over time.")
        else:
            st.info("Start writing your entry to see mood analysis.")

# Tab 2: Analytics
with tab2:
    st.header("Mood Analytics")
    
    # Check if there are entries to analyze
    if st.session_state.entries.empty:
        st.info("No journal entries yet. Start writing to see your mood analytics!")
    else:
        # Date range filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=pd.to_datetime(st.session_state.entries['date'].min()).date()
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=pd.to_datetime(st.session_state.entries['date'].max()).date()
            )
        
        # Filter data by date range
        filtered_entries = st.session_state.entries[
            (pd.to_datetime(st.session_state.entries['date']) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(st.session_state.entries['date']) <= pd.to_datetime(end_date))
        ]
        
        if filtered_entries.empty:
            st.warning("No entries found in the selected date range.")
        else:
            # Display analytics in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Mood History Over Time")
                fig1 = plot_mood_history(filtered_entries)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.subheader("Mood Distribution")
                fig2 = plot_mood_distribution(filtered_entries)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Display some statistics
            st.subheader("Mood Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                most_common_mood = filtered_entries['mood'].mode()[0]
                st.metric("Most Common Mood", most_common_mood)
            
            with col2:
                avg_score = filtered_entries['mood_score'].mean()
                st.metric("Average Mood Score", f"{avg_score:.2f}")
            
            with col3:
                entry_count = len(filtered_entries)
                st.metric("Total Entries", entry_count)

# Tab 3: Entry Management
with tab3:
    st.header("Journal Entries")
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    with col1:
        mood_filter = st.selectbox(
            "Filter by Mood",
            ["All", "Joyful", "Peaceful", "Energetic", "Creative", "Neutral", 
             "Reflective", "Anxious", "Sad", "Angry", "Confused"],
            key="mood_filter"
        )
    
    with col2:
        search_query = st.text_input("Search in titles and content", key="search_query")
    
    # Apply filters
    filtered_entries = st.session_state.entries.copy()
    
    if mood_filter != "All":
        filtered_entries = filtered_entries[filtered_entries['mood'] == mood_filter]
    
    if search_query:
        filtered_entries = filtered_entries[
            filtered_entries['title'].str.contains(search_query, case=False) |
            filtered_entries['content'].str.contains(search_query, case=False)
        ]
    
    # Display entries
    if filtered_entries.empty:
        st.info("No journal entries found with the current filters.")
    else:
        # Sort entries by date (newest first)
        filtered_entries = filtered_entries.sort_values(by='date', ascending=False)
        
        for _, entry in filtered_entries.iterrows():
            with st.expander(f"{entry['date']} - {entry['title']} ({entry['mood']})"):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**Date:** {entry['date']}")
                    st.markdown(f"**Mood:** {entry['mood']} (Score: {entry['mood_score']:.2f})")
                    st.write(entry['content'])
                
                with col2:
                    # Edit button
                    if st.button("Edit", key=f"edit_{entry['id']}"):
                        st.session_state.current_entry_id = entry['id']
                        st.session_state.edit_mode = True
                        st.rerun()
                    
                    # Delete button
                    if st.button("Delete", key=f"delete_{entry['id']}"):
                        if delete_journal_entry(entry['id']):
                            st.success("Entry deleted successfully!")
                            # Reload the journal entries
                            st.session_state.entries = load_journal_entries()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to delete entry.")

st.markdown("---")
st.markdown("MoodJournal - Track your emotional wellbeing with AI-powered insights.")
