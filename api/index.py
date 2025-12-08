import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

from models.chicken_model import ChickenModel
from models.farm_model import FarmModel
from models.ai_model import health_model, production_model, feed_model

app = Flask(__name__, static_folder='../static', template_folder='templates')
CORS(app)

# Initialize the models
chicken_model = ChickenModel()
farm_model = FarmModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chickens', methods=['GET', 'POST'])
def chickens():
    if request.method == 'POST':
        data = request.get_json()
        chicken_id = chicken_model.add_chicken(data)
        return jsonify({"id": chicken_id, "status": "created"}), 201
    else:
        chickens = chicken_model.get_all_chickens()
        return jsonify(chickens)

@app.route('/api/chickens/<int:chicken_id>', methods=['GET', 'PUT', 'DELETE'])
def chicken(chicken_id):
    if request.method == 'GET':
        chicken = chicken_model.get_chicken(chicken_id)
        if chicken:
            # Add AI predictions to the chicken data
            chicken['health_risk'] = health_model.predict_health_risk(chicken)
            chicken['production_prediction'] = production_model.predict_production(chicken)
            return jsonify(chicken)
        else:
            return jsonify({"error": "Chicken not found"}), 404
    elif request.method == 'PUT':
        data = request.get_json()
        chicken_model.update_chicken(chicken_id, data)
        return jsonify({"status": "updated"})
    elif request.method == 'DELETE':
        chicken_model.delete_chicken(chicken_id)
        return jsonify({"status": "deleted"})

@app.route('/api/eggs', methods=['GET', 'POST'])
def eggs():
    if request.method == 'POST':
        data = request.get_json()
        egg_id = farm_model.record_egg_production(data)
        return jsonify({"id": egg_id, "status": "recorded"}), 201
    else:
        eggs = farm_model.get_egg_production()
        return jsonify(eggs)

@app.route('/api/feed', methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        data = request.get_json()
        feed_id = farm_model.record_feed_schedule(data)
        return jsonify({"id": feed_id, "status": "recorded"}), 201
    else:
        feed = farm_model.get_feed_schedule()
        return jsonify(feed)

@app.route('/api/feed/optimize/<int:chicken_id>', methods=['GET'])
def optimize_feed(chicken_id):
    """Get AI-based feed optimization for a specific chicken"""
    optimization = feed_model.optimize_feed_schedule(chicken_id)
    return jsonify(optimization)

@app.route('/api/health', methods=['GET'])
def health():
    health_data = farm_model.get_health_predictions()
    return jsonify(health_data)

@app.route('/api/health', methods=['POST'])
def record_health():
    data = request.get_json()
    health_id = farm_model.record_health_check(data)
    return jsonify({"id": health_id, "status": "recorded"}), 201

@app.route('/api/ai/health/predict/<int:chicken_id>', methods=['GET'])
def predict_health_risk(chicken_id):
    """Get AI-based health risk prediction for a specific chicken"""
    chicken = chicken_model.get_chicken(chicken_id)
    if not chicken:
        return jsonify({"error": "Chicken not found"}), 404
    
    prediction = health_model.predict_health_risk(chicken)
    return jsonify(prediction)

@app.route('/api/ai/production/predict/<int:chicken_id>', methods=['GET'])
def predict_production(chicken_id):
    """Get AI-based production prediction for a specific chicken"""
    chicken = chicken_model.get_chicken(chicken_id)
    if not chicken:
        return jsonify({"error": "Chicken not found"}), 404
    
    prediction = production_model.predict_production(chicken)
    return jsonify(prediction)

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    # Get comprehensive dashboard data
    chickens = chicken_model.get_all_chickens()
    eggs = farm_model.get_egg_production()
    health_records = farm_model.get_health_records()
    
    # Calculate stats
    total_chickens = len(chickens)
    healthy_count = sum(1 for c in chickens if c['health_status'] == 'healthy')
    sick_count = sum(1 for c in chickens if c['health_status'] == 'sick')
    daily_egg_count = sum(1 for e in eggs if e['date'].split('T')[0] == str(datetime.now().date()))
    
    # Find recent health alerts
    recent_health_issues = [hr for hr in health_records 
                           if hr['date'].split('T')[0] == str(datetime.now().date()) 
                           and hr['health_status'] != 'healthy']
    
    # Generate AI insights
    ai_insights = generate_ai_insights(chickens, eggs)
    
    dashboard_data = {
        'total_chickens': total_chickens,
        'healthy_chickens': healthy_count,
        'sick_chickens': sick_count,
        'daily_egg_count': daily_egg_count,
        'health_alerts': len(recent_health_issues),
        'recent_health_records': recent_health_issues[:5],  # Last 5 health records
        'ai_insights': ai_insights
    }
    
    return jsonify(dashboard_data)

def generate_ai_insights(chickens, eggs):
    """Generate AI-based insights for the dashboard"""
    if not chickens:
        return {"message": "Add chickens to get AI insights"}
    
    # Calculate average production
    avg_production = sum([e['quantity'] for e in eggs]) / len(eggs) if eggs else 0
    
    # Count chickens by health risk
    high_risk_count = 0
    for chicken in chickens:
        risk = health_model.predict_health_risk(chicken)
        if risk['risk_level'] == 'high':
            high_risk_count += 1
    
    # Predicted production
    total_predicted = 0
    for chicken in chickens:
        prediction = production_model.predict_production(chicken)
        total_predicted += prediction['predicted_eggs_per_week']
    
    return {
        "high_health_risk_count": high_risk_count,
        "total_predicted_weekly_eggs": round(total_predicted, 2),
        "average_daily_eggs": round(avg_production, 2),
        "feed_optimization_available": len(chickens) > 0,
        "recommendations": [
            f"Monitor {high_risk_count} chickens with high health risk",
            f"Expected weekly production: ~{round(total_predicted)} eggs",
        ]
    }

# For Vercel deployment, we need to export the WSGI application as 'app'
application = app

if __name__ == '__main__':
    # Initialize database on startup
    from models.chicken_model import ChickenModel
    from models.farm_model import FarmModel
    
    print("Initializing database...")
    chicken_model = ChickenModel()
    farm_model = FarmModel()
    print("Database initialized successfully!")
    
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))