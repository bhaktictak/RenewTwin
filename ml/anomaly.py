import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_fitted = False
        
    def fit(self, fleet_data_df):
        features = fleet_data_df[['power_ratio', 'temperature', 'days_since_inspection']].fillna(0)
        self.model.fit(features)
        self.is_fitted = True
        
    def detect(self, asset_dict):
        if not self.is_fitted:
            return 0.5 # Default score
            
        features = pd.DataFrame([{
            'power_ratio': asset_dict.get('power_ratio', 1.0),
            'temperature': asset_dict.get('temperature', 25.0),
            'days_since_inspection': asset_dict.get('days_since_inspection', 0)
        }])
        
        # decision_function returns negative for anomalies
        score = self.model.decision_function(features)[0]
        # Normalize to 0-1 (higher = more anomalous)
        norm_score = 1 - (score - (-0.5)) / (0.5 - (-0.5))
        return float(np.clip(norm_score, 0, 1))

def generate_demo_scores(n_assets):
    # SYNTHETIC DEMO data
    return np.random.uniform(0, 0.8, n_assets).tolist()

if __name__ == '__main__':
    # SYNTHETIC TEST
    detector = AnomalyDetector()
    df = pd.DataFrame({
        'power_ratio': np.random.normal(1, 0.1, 100),
        'temperature': np.random.normal(30, 5, 100),
        'days_since_inspection': np.random.uniform(0, 365, 100)
    })
    detector.fit(df)
    score = detector.detect({'power_ratio': 0.5, 'temperature': 60, 'days_since_inspection': 400})
    print(f"Demo Anomaly Score (SYNTHETIC): {score}")
