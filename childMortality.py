import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths, column_mappings

def clean_child_mortality_data(df):
    """Clean and prepare child mortality data"""
    # Create deep copy
    df = df.copy(deep=True)
    
    # Rename columns for and drop unnecessary ones
    df = df.rename(columns={
        'Entity': 'Country',
        'Observation value - Indicator: Under-five mortality rate - Sex: Total - Wealth quintile: Total - Unit of measure: Deaths per 100 live births': 'Under_five_mortality_rate'
    })
    df = df.drop(columns=['Code'])
    
    # Handle missing values
    df['Under_five_mortality_rate'] = df['Under_five_mortality_rate'].fillna(
        df['Under_five_mortality_rate'].median()
    )
    
    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)
    
    # Filter for African countries
    df = df[df['Country'].isin(african_countries)]
    
    return df

# Load and process data
def get_child_mortality_data():
    """Load and process child mortality data"""
    # Load data
    child_mortality_rate = pd.read_csv(file_paths['child_mortality'])
    child_mortality_africa = clean_child_mortality_data(child_mortality_rate)
    
    return child_mortality_africa

# Create visualization
def display_visualizations(data):
    """Create and display visualizations"""
    fig = px.line(
        data, 
        x='Year', 
        y='Under_five_mortality_rate', 
        color='Country',
        markers=True,
        title='Child Mortality Rate Trends in African Countries'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Under-five mortality rate',
        legend_title='Country'
    )

    fig.show()

if __name__ == "__main__":
    data = get_child_mortality_data()
    display_visualizations(data)