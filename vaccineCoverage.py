import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths

def clean_vaccine_coverage_data(df):
    """Clean and prepare vaccine coverage data"""
    # Create deep copy
    df = df.copy(deep=True)
    
    # Rename columns and drop unnecessary ones
    df = df.rename(columns={'Entity': 'Country'})
    df = df.drop(columns=['Code'])

    # Handle missing values by replacing missing values in vaccination coverage columns with 0
    vaccination_cols = [col for col in df.columns if '(% of one-year-olds immunized)' in col]
    df[vaccination_cols] = df[vaccination_cols].fillna(0)

    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)

    # Filter for African countries
    df = df[df['Country'].isin(african_countries)]

    return df

# Load and process data
def get_vaccine_coverage_data():
    """Load and process vaccine coverage data"""
    # Load data
    vaccine_coverage = pd.read_csv(file_paths['vaccination'])
    
    # Clean data
    vaccine_coverage_africa = clean_vaccine_coverage_data(vaccine_coverage)

    return vaccine_coverage_africa

# Create visualization
def display_visualizations(data):
    """Create and display visualizations"""
    for col in data.columns:
        if '(% of one-year-olds immunized)' in col:
            fig = px.line(
                data, 
                x='Year', 
                y=col, 
                color='Country',
                markers=True,
                title=f'Vaccination Coverage: {col.split("(")[0]} in African Countries'
            )

            fig.update_layout(
                xaxis_title='Year',
                yaxis_title=col,
                legend_title='Country'
            )

            fig.show()

if __name__ == "__main__":
    data = get_vaccine_coverage_data()
    display_visualizations(data)