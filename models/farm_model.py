import sqlite3
import os
from datetime import datetime
import json

DATABASE = 'chicken_farm.db'

class FarmModel:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Initialize the database with farm-related tables"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Egg production table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS egg_production (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chicken_id INTEGER,
                date TEXT,
                quantity INTEGER,
                notes TEXT
            )
        ''')
        
        # Feed schedule table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feed_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chicken_id INTEGER,
                feed_type TEXT,
                scheduled_time TEXT,
                amount REAL,
                notes TEXT
            )
        ''')
        
        # Health records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chicken_id INTEGER,
                date TEXT,
                health_status TEXT,
                symptoms TEXT,
                treatment TEXT,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_egg_production(self, data):
        """Record egg production"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO egg_production (chicken_id, date, quantity, notes)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('chicken_id'),
            data.get('date', datetime.now().isoformat()),
            data.get('quantity', 0),
            data.get('notes', '')
        ))
        egg_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return egg_id
    
    def get_egg_production(self):
        """Get all egg production records"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM egg_production ORDER BY date DESC')
        records = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'chicken_id': row[1],
                'date': row[2],
                'quantity': row[3],
                'notes': row[4]
            } for row in records
        ]
    
    def record_feed_schedule(self, data):
        """Record feed schedule"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feed_schedule (chicken_id, feed_type, scheduled_time, amount, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('chicken_id'),
            data.get('feed_type', ''),
            data.get('scheduled_time'),
            data.get('amount', 0),
            data.get('notes', '')
        ))
        feed_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return feed_id
    
    def get_feed_schedule(self):
        """Get all feed schedule records"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM feed_schedule')
        records = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'chicken_id': row[1],
                'feed_type': row[2],
                'scheduled_time': row[3],
                'amount': row[4],
                'notes': row[5]
            } for row in records
        ]
    
    def record_health_check(self, data):
        """Record health check"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO health_records (chicken_id, date, health_status, symptoms, treatment, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('chicken_id'),
            data.get('date', datetime.now().isoformat()),
            data.get('health_status'),
            data.get('symptoms', ''),
            data.get('treatment', ''),
            data.get('notes', '')
        ))
        health_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return health_id
    
    def get_health_records(self, chicken_id=None):
        """Get health records, optionally for a specific chicken"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        if chicken_id:
            cursor.execute('SELECT * FROM health_records WHERE chicken_id = ? ORDER BY date DESC', (chicken_id,))
        else:
            cursor.execute('SELECT * FROM health_records ORDER BY date DESC')
            
        records = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'chicken_id': row[1],
                'date': row[2],
                'health_status': row[3],
                'symptoms': row[4],
                'treatment': row[5],
                'notes': row[6]
            } for row in records
        ]
    
    def get_health_predictions(self):
        """AI prediction for health issues - basic implementation"""
        # This would be more sophisticated in a real app with ML models
        # For now, we'll return some basic predictions based on health records
        health_records = self.get_health_records()
        
        # Count chickens with health issues recently
        recent_issues = [record for record in health_records if record['date'] >= str(datetime.now().date()) and record['health_status'] != 'healthy']
        
        # Return some basic insights
        predictions = {
            "total_chickens_monitored": len(set([record['chicken_id'] for record in health_records])),
            "chickens_with_recent_issues": len(set([record['chicken_id'] for record in recent_issues])),
            "recent_health_records": recent_issues[:5],  # Last 5 records
            "recommendation": "Monitor chickens with recent health issues more closely"
        }
        
        return predictions