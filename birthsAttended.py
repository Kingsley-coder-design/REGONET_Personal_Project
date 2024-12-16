import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths

def clean_births_attended_data(df):
    """Clean and prepare births attended data"""
    # Create deep copy
    df = df.copy(deep=True)
    
    # Rename columns and drop unnecessary ones
    df = df.rename(columns={
        'Entity': 'Country', 
        'Births attended by skilled health staff (% of total)': 'Births_attended_by_skilled_staff'
    })
    df = df.drop(columns=['Code'])

    # Handle missing values
    df['Births_attended_by_skilled_staff'] = df['Births_attended_by_skilled_staff'].fillna(
        df['Births_attended_by_skilled_staff'].median()
    )

    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)

    # Filter for African countries
    df = df[df['Country'].isin(african_countries)]

    return df

# Load and process data
def get_births_attended_data():
    """Load and process births attended data"""
    # Load data
    births_attended = pd.read_csv(file_paths['births_attended'])

    # Clean data
    births_attended_africa = clean_births_attended_data(births_attended)

    return births_attended_africa

# Create visualization
def display_visualizations(data):
    """Create and display visualizations"""
    fig = px.line(
        data, 
        x='Year', 
        y='Births_attended_by_skilled_staff', 
        color='Country',
        markers=True,
        title='Births Attended by Skilled Health Staff in African Countries'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Births attended by skilled health staff (%)',
        legend_title='Country'
    )

    fig.show()

if __name__ == "__main__":
    data = get_births_attended_data()
    display_visualizations(data)