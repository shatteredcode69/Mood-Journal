import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_mood_history(entries_df):
    """
    Generate a line plot showing mood scores over time.
    
    Args:
        entries_df (pandas.DataFrame): DataFrame containing journal entries.
        
    Returns:
        plotly.graph_objects.Figure: A Plotly figure object with the mood history plot.
    """
    # Convert date to datetime
    df = entries_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values(by='date')
    
    # Create the mood history line plot
    fig = px.line(
        df,
        x='date',
        y='mood_score',
        markers=True,
        color_discrete_sequence=['#1f77b4'],
        hover_data=['title', 'mood']
    )
    
    # Add colored points based on mood
    colors = {
        'Joyful': '#2ca02c',     # Green
        'Peaceful': '#17becf',   # Cyan
        'Energetic': '#ff7f0e',  # Orange
        'Creative': '#9467bd',   # Purple
        'Neutral': '#7f7f7f',    # Gray
        'Reflective': '#8c564b', # Brown
        'Anxious': '#e377c2',    # Pink
        'Sad': '#1f77b4',        # Blue
        'Angry': '#d62728',      # Red
        'Confused': '#bcbd22'    # Yellow
    }
    
    for mood, color in colors.items():
        mood_df = df[df['mood'] == mood]
        if not mood_df.empty:
            fig.add_trace(
                go.Scatter(
                    x=mood_df['date'],
                    y=mood_df['mood_score'],
                    mode='markers',
                    marker=dict(color=color, size=10),
                    name=mood,
                    hoverinfo='text',
                    hovertext=[
                        f"Date: {date}<br>Title: {title}<br>Mood: {mood}<br>Score: {score:.2f}"
                        for date, title, mood, score in zip(
                            mood_df['date'].dt.strftime('%Y-%m-%d'),
                            mood_df['title'],
                            mood_df['mood'],
                            mood_df['mood_score']
                        )
                    ]
                )
            )
    
    # Add a horizontal line at score = 0
    fig.add_shape(
        type="line",
        x0=df['date'].min(),
        y0=0,
        x1=df['date'].max(),
        y1=0,
        line=dict(color="lightgray", width=1, dash="dash")
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Mood Score",
        legend_title="Mood",
        hovermode="closest",
        height=400,
        xaxis=dict(
            tickformat="%Y-%m-%d",
            tickangle=-45,
        ),
        yaxis=dict(
            range=[-1.1, 1.1],
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]
        )
    )
    
    return fig

def plot_mood_distribution(entries_df):
    """
    Generate a pie chart showing the distribution of moods.
    
    Args:
        entries_df (pandas.DataFrame): DataFrame containing journal entries.
        
    Returns:
        plotly.graph_objects.Figure: A Plotly figure object with the mood distribution plot.
    """
    # Count the occurrences of each mood
    mood_counts = entries_df['mood'].value_counts().reset_index()
    mood_counts.columns = ['mood', 'count']
    
    # Define colors for each mood
    colors = {
        'Joyful': '#2ca02c',     # Green
        'Peaceful': '#17becf',   # Cyan
        'Energetic': '#ff7f0e',  # Orange
        'Creative': '#9467bd',   # Purple
        'Neutral': '#7f7f7f',    # Gray
        'Reflective': '#8c564b', # Brown
        'Anxious': '#e377c2',    # Pink
        'Sad': '#1f77b4',        # Blue
        'Angry': '#d62728',      # Red
        'Confused': '#bcbd22'    # Yellow
    }
    
    # Create a list of colors based on the moods in the data
    mood_colors = [colors.get(mood, '#7f7f7f') for mood in mood_counts['mood']]
    
    # Create the pie chart
    fig = px.pie(
        mood_counts,
        values='count',
        names='mood',
        color='mood',
        color_discrete_map={mood: color for mood, color in zip(mood_counts['mood'], mood_colors)},
        hole=0.4
    )
    
    # Customize the layout
    fig.update_layout(
        legend_title="Mood",
        height=400,
        showlegend=True
    )
    
    # Update traces
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    return fig