import sqlite3
import os
from datetime import datetime

DATABASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'chicken_farm.db')

class ChickenModel:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Initialize the database with chickens table"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chickens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                breed TEXT,
                age INTEGER,
                health_status TEXT DEFAULT 'healthy',
                date_added TEXT,
                feeding_schedule TEXT,
                notes TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_chicken(self, data):
        """Add a new chicken to the database"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chickens (name, breed, age, health_status, date_added, feeding_schedule, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name', ''),
            data.get('breed', ''),
            data.get('age', 0),
            data.get('health_status', 'healthy'),
            datetime.now().isoformat(),
            data.get('feeding_schedule', ''),
            data.get('notes', '')
        ))
        chicken_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return chicken_id
    
    def get_all_chickens(self):
        """Get all chickens from the database"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chickens')
        chickens = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        return [
            {
                'id': row[0],
                'name': row[1],
                'breed': row[2],
                'age': row[3],
                'health_status': row[4],
                'date_added': row[5],
                'feeding_schedule': row[6],
                'notes': row[7]
            } for row in chickens
        ]
    
    def get_chicken(self, chicken_id):
        """Get a specific chicken by ID"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chickens WHERE id = ?', (chicken_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'breed': row[2],
                'age': row[3],
                'health_status': row[4],
                'date_added': row[5],
                'feeding_schedule': row[6],
                'notes': row[7]
            }
        return None
    
    def update_chicken(self, chicken_id, data):
        """Update a specific chicken"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE chickens
            SET name=?, breed=?, age=?, health_status=?, feeding_schedule=?, notes=?
            WHERE id=?
        ''', (
            data.get('name', ''),
            data.get('breed', ''),
            data.get('age', 0),
            data.get('health_status', 'healthy'),
            data.get('feeding_schedule', ''),
            data.get('notes', ''),
            chicken_id
        ))
        conn.commit()
        conn.close()
    
    def delete_chicken(self, chicken_id):
        """Delete a specific chicken"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM chickens WHERE id = ?', (chicken_id,))
        conn.commit()
        conn.close()