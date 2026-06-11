import sqlite3
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ExerciseRecord:
    id: Optional[int]
    distance: float
    timestamp: datetime
    
    def __init__(self, id: Optional[int], distance: float, timestamp: datetime):
        self.id = id
        self.distance = distance
        self.timestamp = timestamp
        
    def to_dict(self):
        return {
            'id': self.id,
            'distance': self.distance,
            'timestamp': self.timestamp.isoformat()
        }

class ExerciseDatabase:
    def __init__(self, db_path: str = "exercise_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercise_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                distance REAL NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_session(self, distance: float) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now()
        cursor.execute(
            "INSERT INTO exercise_sessions (distance, timestamp) VALUES (?, ?)",
            (distance, timestamp)
        )
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
        
    def get_all_sessions(self) -> List[ExerciseRecord]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, distance, timestamp FROM exercise_sessions ORDER BY timestamp"
        )
        
        records = []
        for row in cursor.fetchall():
            records.append(ExerciseRecord(row[0], row[1], datetime.fromisoformat(row[2])))
            
        conn.close()
        return records
    
    def get_daily_totals(self) -> List[tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(timestamp) as date, SUM(distance) as total_distance
            FROM exercise_sessions 
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
        
    def get_monthly_totals(self) -> List[tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT strftime('%Y-%m', timestamp) as month, SUM(distance) as total_distance
            FROM exercise_sessions 
            GROUP BY strftime('%Y-%m', timestamp)
            ORDER BY month
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results