import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths

def clean_youth_mortality_data(df):
    """Clean and prepare youth mortality data"""
    # Create deep copy
    df = df.copy(deep=True)
    
    # Handle missing values
    df['Under-fifteen mortality rate'] = df['Under-fifteen mortality rate'].fillna(
        df['Under-fifteen mortality rate'].median()
    )
    
    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)
    
    # Rename columns and drop unnecessary ones
    df = df.rename(columns={'Entity': 'Country'})
    df = df.drop(columns=['Code'])
    
    # Filter for African countries
    df = df[df['Country'].isin(african_countries)]
    
    return df

# Load and process data
def get_youth_mortality_data():
    """Load and process youth mortality data"""
    # Load data
    youth_mortality_rate = pd.read_csv(file_paths['youth_mortality'])
    
    # Clean data
    youth_mortality_africa = clean_youth_mortality_data(youth_mortality_rate)
    
    return youth_mortality_africa

# Create visualization
def display_visualizations(data):
    """Create and display visualizations"""
    fig = px.line(
        data, 
        x='Year', 
        y='Under-fifteen mortality rate', 
        color='Country',  # Changed from 'Entity' to 'Country'
        markers=True,
        title='Youth Mortality Rate Trends in African Countries'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Under-fifteen mortality rate',
        legend_title='Country'
    )

    fig.show()

if __name__ == "__main__":
    data = get_youth_mortality_data()
    display_visualizations(data)