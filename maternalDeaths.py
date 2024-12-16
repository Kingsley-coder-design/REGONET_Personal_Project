import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths

def clean_maternal_deaths_data(df):
    """Clean and prepare maternal deaths data"""
    # Create deep copy
    df = df.copy(deep=True)
    
    # Rename columns and drop unnecessary ones
    df = df.rename(columns={'Entity': 'Country'})
    df = df.drop(columns=['Code','959828-annotations'])

    # Handle missing values
    df['Estimated maternal deaths'] = df['Estimated maternal deaths'].fillna(
        df['Estimated maternal deaths'].median()
    )

    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)

    # Filter for African countries
    df = df[df['Country'].isin(african_countries)]

    return df

# Load and process data
def get_maternal_deaths_data():
    """Load and process maternal deaths data"""
    # Load data
    maternal_deaths = pd.read_csv(file_paths['maternal_deaths'])
    maternal_deaths_africa = clean_maternal_deaths_data(maternal_deaths)
    
    return maternal_deaths_africa

# Create visualization
def display_visualizations(data):
    """Create and display visualizations"""
    fig = px.line(
        data, 
        x='Year', 
        y='Estimated maternal deaths', 
        color='Country',
        markers=True,
        title='Estimated Maternal Deaths in African Countries'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Estimated Maternal Deaths',
        legend_title='Country'
    )

    fig.show()

if __name__ == "__main__":
    data = get_maternal_deaths_data()
    display_visualizations(data)