"""
Indian District Indicators Data Generator
Generates synthetic data mimicking Census, NFHS, and agricultural statistics
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Indian states and districts (sample)
STATES_DISTRICTS = {
    'Uttar Pradesh': ['Lucknow', 'Varanasi', 'Agra', 'Kanpur', 'Prayagraj', 'Gorakhpur', 'Mathura', 'Bareilly'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Thane', 'Kolhapur'],
    'Bihar': ['Patna', 'Gaya', 'Muzaffarpur', 'Bhagalpur', 'Darbhanga', 'Purnia', 'Araria'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer', 'Bikaner', 'Alwar'],
    'Madhya Pradesh': ['Bhopal', 'Indore', 'Gwalior', 'Jabalpur', 'Ujjain', 'Sagar', 'Rewa'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli'],
    'Karnataka': ['Bengaluru', 'Mysuru', 'Hubli', 'Mangaluru', 'Belagavi', 'Gulbarga'],
    'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Berhampur', 'Sambalpur', 'Puri', 'Kalahandi'],
    'West Bengal': ['Kolkata', 'Howrah', 'Asansol', 'Siliguri', 'Durgapur', 'Murshidabad'],
    'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Tirupati', 'Nellore', 'Kurnool'],
}

# State development index (for realistic correlations)
STATE_DEV_INDEX = {
    'Tamil Nadu': 0.8, 'Karnataka': 0.75, 'Maharashtra': 0.72, 'Andhra Pradesh': 0.65,
    'West Bengal': 0.6, 'Rajasthan': 0.55, 'Madhya Pradesh': 0.5, 'Odisha': 0.48,
    'Uttar Pradesh': 0.45, 'Bihar': 0.4
}

def generate_district_data():
    """Generate comprehensive district-level indicators"""
    records = []
    district_id = 1

    for state, districts in STATES_DISTRICTS.items():
        dev_index = STATE_DEV_INDEX[state]

        for district in districts:
            # Add district-level randomness
            local_dev = dev_index + np.random.uniform(-0.15, 0.15)
            local_dev = max(0.2, min(0.95, local_dev))

            # Population (lakhs)
            population = np.random.uniform(10, 80) * (1 + (1 - local_dev) * 0.5)

            # Literacy rate (correlated with development)
            literacy_rate = 50 + local_dev * 40 + np.random.normal(0, 5)
            literacy_rate = max(40, min(98, literacy_rate))

            # Female literacy (typically lower)
            female_literacy = literacy_rate - np.random.uniform(5, 15)
            female_literacy = max(35, min(95, female_literacy))

            # Health indicators
            infant_mortality = 80 - local_dev * 50 + np.random.normal(0, 8)
            infant_mortality = max(10, min(80, infant_mortality))

            maternal_mortality = 300 - local_dev * 200 + np.random.normal(0, 30)
            maternal_mortality = max(50, min(350, maternal_mortality))

            # Immunization coverage
            immunization = 40 + local_dev * 50 + np.random.normal(0, 8)
            immunization = max(30, min(98, immunization))

            # Malnutrition (stunting %)
            stunting = 60 - local_dev * 40 + np.random.normal(0, 5)
            stunting = max(15, min(60, stunting))

            # Access to clean water (%)
            clean_water = 40 + local_dev * 50 + np.random.normal(0, 8)
            clean_water = max(30, min(98, clean_water))

            # Sanitation coverage (%)
            sanitation = 30 + local_dev * 60 + np.random.normal(0, 10)
            sanitation = max(20, min(100, sanitation))

            # Agricultural data
            crop_yield = 20 + local_dev * 20 + np.random.normal(0, 5)  # quintal/hectare
            irrigated_area = 30 + local_dev * 50 + np.random.normal(0, 10)  # percentage

            # Income indicators
            per_capita_income = 30000 + local_dev * 120000 + np.random.normal(0, 10000)
            bpl_population = 60 - local_dev * 50 + np.random.normal(0, 8)  # Below poverty line %
            bpl_population = max(5, min(70, bpl_population))

            # Infrastructure
            road_density = 50 + local_dev * 150 + np.random.normal(0, 20)  # km per 100 sq km
            electrification = 60 + local_dev * 35 + np.random.normal(0, 5)
            electrification = max(50, min(100, electrification))

            # Bank/financial access
            bank_branches = int(5 + local_dev * 30 + np.random.normal(0, 5))

            # Education infrastructure
            schools_per_lakh = 80 + local_dev * 60 + np.random.normal(0, 10)
            dropout_rate = 40 - local_dev * 30 + np.random.normal(0, 5)
            dropout_rate = max(5, min(50, dropout_rate))

            records.append({
                'district_id': f'DIST_{district_id:03d}',
                'district_name': district,
                'state': state,
                'population_lakhs': round(population, 2),
                'literacy_rate': round(literacy_rate, 1),
                'female_literacy_rate': round(female_literacy, 1),
                'infant_mortality_rate': round(infant_mortality, 1),
                'maternal_mortality_ratio': round(maternal_mortality, 0),
                'immunization_coverage': round(immunization, 1),
                'stunting_rate': round(stunting, 1),
                'clean_water_access': round(clean_water, 1),
                'sanitation_coverage': round(sanitation, 1),
                'crop_yield': round(crop_yield, 1),
                'irrigated_area_pct': round(irrigated_area, 1),
                'per_capita_income': round(per_capita_income, 0),
                'bpl_population_pct': round(bpl_population, 1),
                'road_density': round(road_density, 1),
                'electrification_pct': round(electrification, 1),
                'bank_branches': bank_branches,
                'schools_per_lakh': round(schools_per_lakh, 0),
                'dropout_rate': round(dropout_rate, 1),
            })
            district_id += 1

    df = pd.DataFrame(records)
    return df

def save_dataset(df, output_dir='../data'):
    """Save generated dataset"""
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(f'{output_dir}/district_indicators.csv', index=False)
    print(f"Saved to {output_dir}/district_indicators.csv")
    print(f"Total districts: {len(df)}")
    print(f"States covered: {df['state'].nunique()}")

if __name__ == "__main__":
    df = generate_district_data()
    save_dataset(df)
    print("\nSample data:")
    print(df.head())
    print("\nIndicator statistics:")
    print(df.describe())
