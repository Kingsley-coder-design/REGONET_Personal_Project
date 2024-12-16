import pandas as pd
import plotly.express as px
from utils import african_countries, file_paths

def clean_causes_death_data(df):
      """Clean and prepare causes of death data"""
      # Create deep copy
      df = df.copy(deep=True)
      
      # Rename columns and drop unnecessary ones
      df = df.rename(columns={
         'Location': 'Country', 
         'Period': 'Year',
         'Dim1': 'Age_group',
         'Dim2': 'Cause_of_death_group',
      })
      df = df.drop(columns=['IndicatorCode', 'Indicator', 'ParentLocationCode', 'Location type', 'SpatialDimValueCode', 'Period type',
                              'IsLatestYear', 'Dim1 type', 'Dim1ValueCode', 'Dim2 type', 'Dim2ValueCode', 'Dim3 type', 'Dim3', 'Dim3ValueCode',
                              'DataSourceDimValueCode', 'DataSource', 'FactValueNumericPrefix', 'FactValueNumeric', 'FactValueUoM', 
                              'FactValueNumericLowPrefix', 'FactValueNumericLow', 'FactValueNumericHighPrefix', 'FactValueNumericHigh',
                              'FactValueTranslationID', 'FactComments', 'Language', 'DateModified', 'ValueType', 'ParentLocation'
                           ])

      # # Handle missing values (if any)
      # df['Country', 'Year', 'Age group', 'Cause of death group'] = df['Country', 'Year', 'Age group', 'Cause of death group'].fillna(
      #    df['Country', 'Year', 'Age group', 'Cause of death group'].median()
      # )

      # Convert Year to integer
      df['Year'] = df['Year'].astype(int)

      # Filter for African countries
      df = df[df['Country'].isin(african_countries)]

      return df

# Load and process data
def get_causes_death_data():
      """Load and process causes of death data"""
      # Load data
      causes_death = pd.read_csv(file_paths['causes_death'])
      
      # Clean data
      causes_death_africa = clean_causes_death_data(causes_death)

      return causes_death_africa

# Create visualization
def display_visualizations(data):
      """Create and display visualizations"""

      # Group the data by Country, Year, Age group, and Cause of death group
      grouped_data = data.groupby(['Country', 'Year', 'Age_group', 'Cause_of_death_group'])['Value'].sum().reset_index()

      # Print unique countries to verify
      # print(grouped_data['Country'].unique())

      # Select a subset of countries for better visualization
      selected_countries = ['Nigeria', 'South Africa', 'Kenya', 'Ethiopia', 'Egypt']
      grouped_data_subset = grouped_data[grouped_data['Country'].isin(selected_countries)]

      # Create a Bar Chart with Facets
      fig = px.bar(
         grouped_data_subset, 
         x='Cause_of_death_group', 
         y='Value', 
         color='Year',
         facet_col='Country',
         facet_row='Age_group',
         title='Child Mortality Causes in Selected African Countries by Age Group',
         labels={'Value': 'Number of Deaths'}
      )

      # Update layout for better readability
      fig.update_layout(
         height=1500,  # Increased height to accommodate multiple countries
         width=2000,   # Increased width to show more countries
         title_text='Child Mortality Causes Across Selected African Countries by Age Group',
         xaxis_title='Cause of Death',
         yaxis_title='Number of Deaths'
      )

      # Rotate x-axis labels for better readability
      fig.update_xaxes(tickangle=45)

      fig.show()

if __name__ == "__main__":
      data = get_causes_death_data()
      display_visualizations(data)