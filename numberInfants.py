import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths

def clean_number_infants_data(df):
    """Clean and prepare number of infant deaths data"""
    # Create deep copy
    df = df.copy(deep=True)
    
    # Rename columns and drop unnecessary ones
    df = df.rename(columns={
        'Entity': 'Country', 
        'Deaths - Sex: all - Age: 0 - Variant: estimates': 'Number_of_infant_deaths'
    })
    df = df.drop(columns=['Code'])

    # Handle missing values
    df['Number_of_infant_deaths'] = df['Number_of_infant_deaths'].fillna(
        df['Number_of_infant_deaths'].median()
    )

    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)

    # Filter for African countries
    df = df[df['Country'].isin(african_countries)]

    return df

# Load and process data
def get_number_infants_data():
    """Load and process number of infant deaths data"""
    # Load data
    infant_deaths = pd.read_csv(file_paths['infant_deaths'])
    
    # Clean data
    infant_deaths_africa = clean_number_infants_data(infant_deaths)

    return infant_deaths_africa

# Create visualization
def display_visualizations(data):
    """Create and display visualizations"""
    fig = px.line(
        data, 
        x='Year', 
        y='Number_of_infant_deaths', 
        color='Country',
        markers=True,
        title='Number of Infant Deaths in African Countries'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of Infant Deaths',
        legend_title='Country'
    )

    fig.show()

if __name__ == "__main__":
    data = get_number_infants_data()
    display_visualizations(data)