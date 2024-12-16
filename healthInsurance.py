import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths

def clean_health_insurance_data(df):
    """Clean and prepare health insurance data"""
    # Create deep copy
    df = df.copy(deep=True)
    
    # Rename columns and drop unnecessary ones
    df = df.rename(columns={
        'Entity': 'Country', 
        'Share of population covered by health insurance (ILO (2014))': 'Health_insurance_coverage'
    })
    df = df.drop(columns=['Code'])

    # Handle missing values
    df['Health_insurance_coverage'] = df['Health_insurance_coverage'].fillna(
        df['Health_insurance_coverage'].median()
    )

    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)

    # Filter for African countries
    df = df[df['Country'].isin(african_countries)]

    return df

# Load and process data
def get_health_insurance_data():
    """Load and process health insurance data"""
    # Load data
    health_insurance = pd.read_csv(file_paths['health_protection'])
    
    # Clean data
    health_insurance_africa = clean_health_insurance_data(health_insurance)

    return health_insurance_africa

# Create visualization
def display_visualizations(data):
    """Create and display visualizations"""
    fig = px.bar(
        data, 
        x='Country', 
        y='Health_insurance_coverage', 
        color='Country',
        title='Health Insurance Coverage in African Countries'
    )

    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Health insurance coverage (%)',
        legend_title='Country'
    )

    fig.show()

if __name__ == "__main__":
    data = get_health_insurance_data()
    display_visualizations(data)
