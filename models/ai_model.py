from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib
import sqlite3
import os
from datetime import datetime, timedelta
import json
from models.chicken_model import ChickenModel
from models.farm_model import FarmModel

class HealthPredictionModel:
    """
    AI model for predicting health issues in chickens
    """
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.chicken_model = ChickenModel()
        self.farm_model = FarmModel()

    def prepare_data(self):
        """
        Prepare training data from the database
        """
        # Get chickens and health records from the database
        chickens = self.chicken_model.get_all_chickens()
        health_records = self.farm_model.get_health_records()

        if len(chickens) == 0:
            # If no data exists, create synthetic data for initial training
            np.random.seed(42)
            # Features: age, feeding_frequency, environmental_conditions, previous_health_issues
            X = np.random.rand(100, 4) * 100
            # Target: health_status (0 = healthy, 1 = needs attention)
            y = (X[:, 0]*0.1 + X[:, 1]*0.2 + X[:, 2]*0.3 + X[:, 3]*0.4 + np.random.rand(100)*20 > 50).astype(int)
            return X, y

        # Create features from real data
        X = []
        y = []

        for chicken in chickens:
            age = chicken.get('age', 0)
            # Calculate if the chicken has had health issues recently
            recent_issues = len([hr for hr in health_records if hr['chicken_id'] == chicken['id'] and
                                (datetime.now() - datetime.fromisoformat(hr['date'].split('.')[0])).days <= 14])

            # Features: [age, recent_health_issues, days_since_added]
            try:
                days_since_added = (datetime.now() - datetime.fromisoformat(chicken['date_added'].split('.')[0])).days
            except:
                days_since_added = 0

            # Health status is a target: 0=healthy, 1=unhealthy
            status = 0 if chicken['health_status'] == 'healthy' else 1

            X.append([age, recent_issues, days_since_added, 1 if chicken['health_status'] != 'healthy' else 0])
            y.append(status)

        if len(X) > 0:
            return np.array(X), np.array(y)
        else:
            # Fallback to synthetic data if no real data available
            np.random.seed(42)
            X = np.random.rand(50, 4) * 100
            y = (X[:, 0]*0.1 + X[:, 1]*0.2 + X[:, 2]*0.3 + X[:, 3]*0.4 + np.random.rand(50)*20 > 50).astype(int)
            return X, y

    def train_model(self):
        """
        Train the health prediction model
        """
        X, y = self.prepare_data()

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict_health_risk(self, chicken_data):
        """
        Predict health risk for a chicken based on its data
        """
        if not self.is_trained:
            self.train_model()

        # Prepare features from chicken data
        age = chicken_data.get('age', 0)

        # Calculate features based on what we know about the chicken
        features = np.array([[
            age,
            chicken_data.get('recent_health_issues', 0),
            chicken_data.get('days_since_added', 0),
            1 if chicken_data.get('health_status') != 'healthy' else 0
        ]])

        # Scale features
        features_scaled = self.scaler.transform(features)

        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]

        risk_level = "high" if prediction == 1 else "low"
        probability_value = float(probability[1]) if prediction == 1 else float(probability[0])

        return {
            "risk_level": risk_level,
            "probability": probability_value,
            "needs_attention": bool(prediction),
            "recommendation": "Monitor closely" if prediction == 1 else "Continue regular care"
        }

class ProductionPredictionModel:
    """
    AI model for predicting egg production
    """
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self.chicken_model = ChickenModel()
        self.farm_model = FarmModel()

    def prepare_data(self):
        """
        Prepare training data for production prediction
        """
        # Get chickens and egg production records from the database
        chickens = self.chicken_model.get_all_chickens()
        egg_records = self.farm_model.get_egg_production()

        if len(chickens) == 0 or len(egg_records) == 0:
            # If no data exists, create synthetic data for initial training
            np.random.seed(42)
            # Features: age, season, health_status, feeding_amount
            X = np.random.rand(100, 4) * 100
            # Target: egg production count
            y = X[:, 0] * 0.5 + X[:, 2] * 0.3 + X[:, 3] * 0.4 + np.random.rand(100) * 10
            return X, y

        # Create features from real data
        X = []
        y = []

        for chicken in chickens:
            age = chicken.get('age', 0)

            # Calculate weekly egg production for this chicken
            weekly_production = len([er for er in egg_records if er['chicken_id'] == chicken['id']])

            # Features: [age, health_status_score, days_since_added, breed_factor]
            try:
                days_since_added = (datetime.now() - datetime.fromisoformat(chicken['date_added'].split('.')[0])).days
            except:
                days_since_added = 0

            # Health status score (0=healthy, 1=sick, 0.5=recovery)
            health_score = 0
            if chicken['health_status'] == 'sick':
                health_score = 1
            elif chicken['health_status'] == 'recovery':
                health_score = 0.5

            # Breed factor (simplified)
            breed_factor = 1.0  # Default
            if 'rhode' in (chicken.get('breed', '') or '').lower():
                breed_factor = 1.2
            elif 'sussex' in (chicken.get('breed', '') or '').lower():
                breed_factor = 1.1

            X.append([age, health_score, days_since_added, breed_factor])
            y.append(weekly_production)

        if len(X) > 0:
            return np.array(X), np.array(y)
        else:
            # Fallback to synthetic data if no real data available
            np.random.seed(42)
            X = np.random.rand(50, 4) * 100
            y = X[:, 0] * 0.5 + X[:, 2] * 0.3 + X[:, 3] * 0.4 + np.random.rand(50) * 10
            return X, y

    def train_model(self):
        """
        Train the production prediction model
        """
        X, y = self.prepare_data()

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict_production(self, chicken_data):
        """
        Predict egg production for a chicken
        """
        if not self.is_trained:
            self.train_model()

        age = chicken_data.get('age', 0)

        # Health status score
        health_score = 0
        if chicken_data.get('health_status') == 'sick':
            health_score = 1
        elif chicken_data.get('health_status') == 'recovery':
            health_score = 0.5

        # Days since added
        days_since_added = chicken_data.get('days_since_added', 0)

        # Breed factor
        breed_factor = 1.0
        breed = chicken_data.get('breed', '')
        if 'rhode' in breed.lower():
            breed_factor = 1.2
        elif 'sussex' in breed.lower():
            breed_factor = 1.1

        # Prepare features
        features = np.array([[age, health_score, days_since_added, breed_factor]])

        # Scale features
        features_scaled = self.scaler.transform(features)

        prediction = self.model.predict(features_scaled)[0]

        return {
            "predicted_eggs_per_week": max(0, float(prediction)),
            "confidence": 0.8 if self.is_trained else 0.5  # Higher confidence if trained on real data
        }

class FeedOptimizationModel:
    """
    AI model for optimizing feed schedules
    """
    def __init__(self):
        self.chicken_model = ChickenModel()
        self.farm_model = FarmModel()

    def optimize_feed_schedule(self, chicken_id):
        """
        Provide feed optimization recommendations for a specific chicken
        """
        chicken = self.chicken_model.get_chicken(chicken_id)
        if not chicken:
            return {"error": "Chicken not found"}

        age = chicken.get('age', 0)
        breed = chicken.get('breed', '').lower()
        health_status = chicken.get('health_status', 'healthy')

        # Base feed amount based on age and breed
        base_feed = 120  # grams per day for adult chickens
        if age < 6:  # Young chick
            base_feed = 30
        elif age < 18:  # Growing chick
            base_feed = 80
        elif age > 72:  # Older hen
            base_feed = 110

        # Adjust based on breed
        if 'rhode' in breed or 'penn' in breed:  # Rhode Island Red, Plymouth Rock
            base_feed *= 1.05

        # Adjust based on health
        if health_status != 'healthy':
            base_feed *= 0.9  # Reduce slightly if not healthy

        # Feed schedule recommendation (2-3 times a day)
        feed_times = ["07:00", "13:00", "18:00"]

        # Calculate portion sizes
        portions = [base_feed * 0.4, base_feed * 0.35, base_feed * 0.25]

        return {
            "recommended_daily_feed": round(base_feed, 2),
            "feed_times": feed_times,
            "portion_sizes": [round(p, 2) for p in portions],
            "feed_type": "Layer feed" if age > 18 else "Grower feed",
            "notes": f"Adjust portions based on actual consumption and health. Increase if egg production is low."
        }

# Singleton instances for the models
health_model = HealthPredictionModel()
production_model = ProductionPredictionModel()
feed_model = FeedOptimizationModel()