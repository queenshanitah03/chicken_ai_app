import numpy as np
from datetime import datetime
from models.chicken_model import ChickenModel
from models.farm_model import FarmModel


class HealthPredictionModel:
    """Lightweight health risk heuristics (NumPy-only)."""
    def __init__(self):
        self.chicken_model = ChickenModel()
        self.farm_model = FarmModel()

    def _compute_score(self, chicken):
        age = float(chicken.get('age', 0))
        recent_issues = float(chicken.get('recent_health_issues', 0))
        health_flag = 1.0 if chicken.get('health_status') != 'healthy' else 0.0

        # Simple weighted score in [0, 1]
        score = 0.4 * (recent_issues / (1 + recent_issues)) + 0.3 * health_flag + 0.3 * min(age / 100.0, 1.0)
        return float(min(max(score, 0.0), 1.0))

    def predict_health_risk(self, chicken_data):
        score = self._compute_score(chicken_data)
        risk_level = 'high' if score >= 0.5 else 'low'
        needs = score >= 0.5
        recommendation = 'Monitor closely' if needs else 'Continue regular care'

        return {
            'risk_level': risk_level,
            'probability': round(score, 3),
            'needs_attention': bool(needs),
            'recommendation': recommendation
        }


class ProductionPredictionModel:
    """Lightweight production heuristics without scikit-learn."""
    def __init__(self):
        self.chicken_model = ChickenModel()
        self.farm_model = FarmModel()

    def predict_production(self, chicken_data):
        age = float(chicken_data.get('age', 0))
        health_status = chicken_data.get('health_status', 'healthy')
        days_since_added = float(chicken_data.get('days_since_added', 0))
        breed = (chicken_data.get('breed') or '').lower()

        # Base productivity by age: peak production around 20-60 weeks
        if age < 18:
            base = 1.0  # young
        elif age <= 72:
            base = 4.0  # adult, eggs per week baseline
        else:
            base = 2.5  # older

        # Health multiplier
        health_mul = 0.6 if health_status == 'sick' else (0.9 if health_status == 'recovery' else 1.0)

        # Breed factor
        breed_factor = 1.0
        if 'rhode' in breed:
            breed_factor = 1.2
        elif 'sussex' in breed:
            breed_factor = 1.1

        # small adjustment for days since added (newer chickens adapt)
        age_factor = 1.0 - min(days_since_added / 365.0, 0.25)

        predicted = max(0.0, base * health_mul * breed_factor * age_factor)

        return {
            'predicted_eggs_per_week': round(float(predicted), 2),
            'confidence': 0.6
        }


class FeedOptimizationModel:
    """Simple feed optimization heuristics retained as before."""
    def __init__(self):
        self.chicken_model = ChickenModel()
        self.farm_model = FarmModel()

    def optimize_feed_schedule(self, chicken_id):
        chicken = self.chicken_model.get_chicken(chicken_id)
        if not chicken:
            return {'error': 'Chicken not found'}

        age = chicken.get('age', 0)
        breed = (chicken.get('breed') or '').lower()
        health_status = chicken.get('health_status', 'healthy')

        base_feed = 120
        if age < 6:
            base_feed = 30
        elif age < 18:
            base_feed = 80
        elif age > 72:
            base_feed = 110

        if 'rhode' in breed or 'penn' in breed:
            base_feed *= 1.05
        if health_status != 'healthy':
            base_feed *= 0.9

        feed_times = ['07:00', '13:00', '18:00']
        portions = [base_feed * 0.4, base_feed * 0.35, base_feed * 0.25]

        return {
            'recommended_daily_feed': round(base_feed, 2),
            'feed_times': feed_times,
            'portion_sizes': [round(p, 2) for p in portions],
            'feed_type': 'Layer feed' if age > 18 else 'Grower feed',
            'notes': 'Adjust portions based on actual consumption and health.'
        }


# Singleton instances preserved for compatibility
health_model = HealthPredictionModel()
production_model = ProductionPredictionModel()
feed_model = FeedOptimizationModel()