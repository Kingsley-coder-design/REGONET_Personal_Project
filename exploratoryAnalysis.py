import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from vaccineCoverage import get_vaccine_coverage_data
from birthsAttended import get_births_attended_data
from causesDeath import get_causes_death_data
from childMortality import get_child_mortality_data
from healthInsurance import get_health_insurance_data
from maternalDeaths import get_maternal_deaths_data
from numberInfants import get_number_infants_data
from youthMortality import get_youth_mortality_data

# Get processed data
births_attended_data = get_births_attended_data()
child_mortality_data = get_child_mortality_data()
health_insurance_data = get_health_insurance_data()
maternal_deaths_data = get_maternal_deaths_data()
number_infants_data = get_number_infants_data()
youth_mortality_data = get_youth_mortality_data()
causes_death_data = get_causes_death_data()
vaccine_coverage_data = get_vaccine_coverage_data()
# print(births_attended_data.head())
# print(child_mortality_data.head())
# print(health_insurance_data.head())
# print(maternal_deaths_data.head())
# print(number_infants_data.head())
# print(youth_mortality_data.head())
# print(causes_death_data.head())
# print(vaccine_coverage_data.head())

# Define vaccine groups with correct column names
vaccine_groups = {
    'Basic Vaccines': [
        'BCG (% of one-year-olds immunized)',
        'DTP3 (% of one-year-olds immunized)',
        'HepB3 (% of one-year-olds immunized)'
    ],
    'Viral Vaccines': [
        'MCV1 (% of one-year-olds immunized)',
        'RCV1 (% of one-year-olds immunized)',
        'YFV (% of one-year-olds immunized)'
    ],
    'Bacterial Vaccines': [
        'Hib3 (% of one-year-olds immunized)',
        'PCV3 (% of one-year-olds immunized)'
    ],
    'Other Vaccines': [
        'IPV1 (% of one-year-olds immunized)',
        'Pol3 (% of one-year-olds immunized)',
        'RotaC (% of one-year-olds immunized)'
    ]
}

def analyze_vaccination_impact():
    """Analyze impact of vaccination on mortality rates"""
    
    # Merge mortality datasets first
    mortality_data = child_mortality_data.merge(
        number_infants_data, on=['Country', 'Year'], how='inner'
    ).merge(
        maternal_deaths_data, on=['Country', 'Year'], how='inner'
    ).merge(
        youth_mortality_data, on=['Country', 'Year'], how='inner'
    )
    
    # Then merge with vaccination data
    merged_data = mortality_data.merge(
        vaccine_coverage_data, on=['Country', 'Year'], how='inner'
    )
    
    # Print column names to verify
    print("Available columns:", merged_data.columns.tolist())
    
    # Define indicators
    mortality_indicators = {
        'Child Mortality': 'Under_five_mortality_rate',
        'Infant Deaths': 'Number_of_infant_deaths',
        'Maternal Deaths': 'Estimated maternal deaths',
        'Youth Mortality': 'Under-fifteen mortality rate'
    }
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    
    for idx, (label, column) in enumerate(mortality_indicators.items(), 1):
        plt.subplot(2, 2, idx)
        
        # Plot mortality trend
        yearly_mortality = merged_data.groupby('Year')[column].mean()
        plt.plot(yearly_mortality.index, yearly_mortality.values, 
                label='Mortality Rate', color='red', marker='o')
        
        # Plot vaccination coverage (using actual column names)
        ax2 = plt.twinx()
        vaccination_cols = [col for col in merged_data.columns if 'immunized' in col]
        for vaccine in vaccination_cols[:3]:  # Plot top 3 vaccines
            yearly_coverage = merged_data.groupby('Year')[vaccine].mean()
            ax2.plot(yearly_coverage.index, yearly_coverage.values, 
                    label=vaccine.split('(')[0], linestyle='--', alpha=0.5)
        
        plt.title(f'{label} vs Vaccination Coverage')
        plt.xlabel('Year')
        plt.ylabel('Mortality Rate')
        ax2.set_ylabel('Vaccination Coverage (%)')
        
        # Add legend
        lines1, labels1 = plt.gca().get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    plt.show()
    
def analyze_birth_attendance_impact():
    """Analyze impact of skilled birth attendance on mortality rates"""
    
    # Merge mortality datasets with births attended data
    analysis_data = child_mortality_data.merge(
        number_infants_data, on=['Country', 'Year'], how='inner'
    ).merge(
        maternal_deaths_data, on=['Country', 'Year'], how='inner'
    ).merge(
        youth_mortality_data, on=['Country', 'Year'], how='inner'
    ).merge(
        births_attended_data, on=['Country', 'Year'], how='inner'
    )
    
    # Define mortality indicators
    mortality_indicators = {
        'Child Mortality': 'Under_five_mortality_rate',
        'Infant Deaths': 'Number_of_infant_deaths',
        'Maternal Deaths': 'Estimated maternal deaths',
        'Youth Mortality': 'Under-fifteen mortality rate'
    }
    
    # Create visualization grid
    plt.figure(figsize=(15, 10))
    
    for idx, (label, column) in enumerate(mortality_indicators.items(), 1):
        plt.subplot(2, 2, idx)
        
        # Create scatter plot with trend line
        sns.regplot(
            data=analysis_data,
            x='Births_attended_by_skilled_staff',
            y=column,
            scatter_kws={'alpha':0.5},
            line_kws={'color': 'red'}
        )
        
        plt.title(f'{label} vs Skilled Birth Attendance')
        plt.xlabel('Births Attended by Skilled Staff (%)')
        plt.ylabel(label)
    
    plt.tight_layout()
    plt.show()
    
    # Calculate and print correlations
    print("\nCorrelation with Skilled Birth Attendance:")
    for label, column in mortality_indicators.items():
        correlation = analysis_data['Births_attended_by_skilled_staff'].corr(analysis_data[column])
        print(f"{label}: {correlation:.3f}")

def analyze_healthcare_mortality():
    """Analyze healthcare indicators and mortality rates"""
    
    # Merge datasets
    analysis_data = causes_death_data.merge(
        births_attended_data, on=['Country', 'Year'], how='inner'
    ).merge(
        vaccine_coverage_data, on=['Country', 'Year'], how='inner'
    ).merge(
        health_insurance_data, on=['Country', 'Year'], how='inner'
    )
    
    # Set plot style and create figure
    plt.style.use('default')  # Use default style instead of seaborn
    fig = plt.figure(figsize=(20, 16))
    plt.subplots_adjust(hspace=0.5, wspace=0.4)
    
    # 1. Healthcare Coverage Time Series
    ax1 = plt.subplot(2, 2, 1)
    top_5_countries = analysis_data.groupby('Country')['Value'].sum().nlargest(5).index
    colors = plt.cm.Set2(np.linspace(0, 1, len(top_5_countries)))
    
    for country, color in zip(top_5_countries, colors):
        data = analysis_data[analysis_data['Country'] == country]
        ax1.plot(data['Year'], 
                data['Births_attended_by_skilled_staff'],
                marker='o', 
                linewidth=2,
                color=color,
                label=country)
    
    ax1.set_title('Healthcare Coverage Trends\n(Top 5 Countries)', 
                 fontsize=14, pad=20)
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Birth Attendance Rate (%)', fontsize=12)
    ax1.legend(bbox_to_anchor=(1.05, 1))
    ax1.grid(True, alpha=0.3)
    
    # 2. Healthcare Metrics Correlation
    ax2 = plt.subplot(2, 2, 2)
    healthcare_metrics = [
        'Births_attended_by_skilled_staff',
        'Health_insurance_coverage',
        'BCG (% of one-year-olds immunized)',
        'DTP3 (% of one-year-olds immunized)',
        'Value'
    ]
    
    correlation_matrix = analysis_data[healthcare_metrics].corr()
    sns.heatmap(correlation_matrix,
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                center=0,
                ax=ax2,
                square=True)
    ax2.set_title('Healthcare Metrics Correlation', fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # 3. Cause of Death Distribution
    ax3 = plt.subplot(2, 2, 3)
    cause_data = analysis_data.groupby('Cause_of_death_group')['Value'].sum()
    top_causes = cause_data.nlargest(8)
    
    bars = sns.barplot(x=top_causes.values,
                      y=top_causes.index,
                      palette='viridis',
                      ax=ax3)
    ax3.set_title('Top Causes of Death', fontsize=14, pad=20)
    ax3.set_xlabel('Number of Deaths', fontsize=12)
    
    # Add value labels to bars
    for i, v in enumerate(top_causes.values):
        ax3.text(v, i, f' {int(v):,}', va='center')
    
    # 4. Healthcare Coverage vs Mortality
    ax4 = plt.subplot(2, 2, 4)
    scatter = sns.scatterplot(data=analysis_data,
                            x='Births_attended_by_skilled_staff',
                            y='Value',
                            hue='Country',
                            size='Health_insurance_coverage',
                            sizes=(50, 400),
                            alpha=0.6,
                            ax=ax4)
    
    ax4.set_title('Healthcare Coverage vs Mortality', fontsize=14, pad=20)
    ax4.set_xlabel('Birth Attendance Rate (%)', fontsize=12)
    ax4.set_ylabel('Number of Deaths', fontsize=12)
    
    plt.tight_layout()
    plt.show()
    
    return analysis_data

if __name__ == "__main__":
    analyze_vaccination_impact()
    analyze_birth_attendance_impact()
    analyze_healthcare_mortality()
