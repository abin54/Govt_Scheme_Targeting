"""
Composite Need/Risk Scoring Engine
Calculates prioritization scores for government scheme targeting
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import joblib
import os

class SchemeTargetingEngine:
    """Engine for calculating district-level need scores"""

    # Indicator weights for different schemes
    SCHEME_WEIGHTS = {
        'PM-KISAN': {
            'bpl_population_pct': 0.25,
            'crop_yield': -0.15,  # Negative = lower is worse
            'irrigated_area_pct': -0.20,
            'per_capita_income': -0.25,
            'bank_branches': -0.15
        },
        'Health': {
            'infant_mortality_rate': 0.25,
            'maternal_mortality_ratio': 0.20,
            'immunization_coverage': -0.15,
            'stunting_rate': 0.20,
            'clean_water_access': -0.10,
            'sanitation_coverage': -0.10
        },
        'Education': {
            'literacy_rate': -0.25,
            'female_literacy_rate': -0.25,
            'schools_per_lakh': -0.15,
            'dropout_rate': 0.20,
            'bpl_population_pct': 0.15
        },
        'Infrastructure': {
            'road_density': -0.20,
            'electrification_pct': -0.25,
            'clean_water_access': -0.20,
            'sanitation_coverage': -0.20,
            'bank_branches': -0.15
        }
    }

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.clusterer = None

    def calculate_need_score(self, df, scheme='Health'):
        """Calculate composite need score for a specific scheme"""
        df = df.copy()
        weights = self.SCHEME_WEIGHTS.get(scheme, self.SCHEME_WEIGHTS['Health'])

        # Normalize all numeric columns
        numeric_cols = [col for col in weights.keys() if col in df.columns]

        # Scale each indicator
        for col in numeric_cols:
            df[f'{col}_scaled'] = self.scaler.fit_transform(df[[col]])

        # Calculate weighted score
        score = np.zeros(len(df))
        for col, weight in weights.items():
            if col in df.columns:
                if weight > 0:
                    # Higher value = higher need
                    score += weight * df[f'{col}_scaled']
                else:
                    # Lower value = higher need (inverted)
                    score += abs(weight) * (1 - df[f'{col}_scaled'])

        # Normalize final score to 0-100
        df[f'{scheme}_need_score'] = (score - score.min()) / (score.max() - score.min()) * 100

        return df

    def calculate_all_scores(self, df):
        """Calculate need scores for all schemes"""
        for scheme in self.SCHEME_WEIGHTS.keys():
            df = self.calculate_need_score(df, scheme)
        return df

    def cluster_districts(self, df, n_clusters=5):
        """Cluster districts based on overall development indicators"""
        feature_cols = [
            'literacy_rate', 'infant_mortality_rate', 'per_capita_income',
            'bpl_population_pct', 'electrification_pct', 'sanitation_coverage'
        ]

        X = df[feature_cols].copy()
        X_scaled = self.scaler.fit_transform(X)

        self.clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['cluster'] = self.clusterer.fit_predict(X_scaled)

        # Label clusters based on average development
        cluster_means = df.groupby('cluster')['per_capita_income'].mean().sort_values()
        cluster_labels = {
            cluster_means.index[0]: 'Very Low Development',
            cluster_means.index[1]: 'Low Development',
            cluster_means.index[2]: 'Medium Development',
            cluster_means.index[3]: 'High Development',
            cluster_means.index[4]: 'Very High Development'
        }
        df['development_category'] = df['cluster'].map(cluster_labels)

        return df

    def prioritize_districts(self, df, scheme, top_n=20):
        """Get top N priority districts for a scheme"""
        score_col = f'{scheme}_need_score'
        if score_col not in df.columns:
            df = self.calculate_need_score(df, scheme)

        priority_df = df.nlargest(top_n, score_col)[
            ['district_id', 'district_name', 'state', score_col, 'population_lakhs']
        ]
        priority_df['priority_rank'] = range(1, len(priority_df) + 1)

        return priority_df

    def simulate_allocation(self, df, scheme, total_budget, allocation_method='proportional'):
        """Simulate budget allocation based on need scores"""
        score_col = f'{scheme}_need_score'
        if score_col not in df.columns:
            df = self.calculate_need_score(df, scheme)

        df = df.copy()

        if allocation_method == 'proportional':
            # Allocate proportional to need score
            total_score = df[score_col].sum()
            df['allocated_budget'] = (df[score_col] / total_score) * total_budget

        elif allocation_method == 'per_capita':
            # Per capita allocation weighted by need
            weighted_pop = df['population_lakhs'] * df[score_col]
            total_weighted = weighted_pop.sum()
            df['allocated_budget'] = (weighted_pop / total_weighted) * total_budget

        elif allocation_method == 'equal':
            # Equal allocation to top 50% needy districts
            median_score = df[score_col].median()
            eligible = df[df[score_col] >= median_score]
            per_district = total_budget / len(eligible)
            df['allocated_budget'] = np.where(
                df[score_col] >= median_score, per_district, 0
            )

        df['per_capita_allocation'] = df['allocated_budget'] / (df['population_lakhs'] * 100000) * 100000

        return df

def main():
    """Run scoring engine"""
    print("="*60)
    print("GOVERNMENT SCHEME TARGETING ENGINE")
    print("="*60)

    # Load data
    df = pd.read_csv('../data/district_indicators.csv')
    print(f"Loaded {len(df)} districts")

    # Initialize engine
    engine = SchemeTargetingEngine()

    # Calculate all scores
    df = engine.calculate_all_scores(df)

    # Cluster districts
    df = engine.cluster_districts(df)

    # Save processed data
    os.makedirs('../data', exist_ok=True)
    df.to_csv('../data/district_scores.csv', index=False)
    print("\nSaved scored data to ../data/district_scores.csv")

    # Print summaries
    for scheme in engine.SCHEME_WEIGHTS.keys():
        print(f"\n{scheme} Scheme - Top 10 Priority Districts:")
        priority = engine.prioritize_districts(df, scheme, top_n=10)
        print(priority.to_string(index=False))

    # Simulate allocation
    print("\n" + "="*60)
    print("BUDGET ALLOCATION SIMULATION")
    print("="*60)

    allocated = engine.simulate_allocation(df, 'Health', total_budget=10000)  # 10000 crores
    top_allocations = allocated.nlargest(10, 'allocated_budget')[
        ['district_name', 'state', 'Health_need_score', 'allocated_budget']
    ]
    print("\nTop 10 allocations (Health scheme, Rs. 10000 Cr budget):")
    print(top_allocations.to_string(index=False))

if __name__ == "__main__":
    main()
