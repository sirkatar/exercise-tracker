import sqlite3
from datetime import datetime, date
from typing import List, Tuple
from models.exercise_model import ExerciseRecord

class DatabaseService:
    def __init__(self, db_path: str = "exercise_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for exercise sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercise_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                distance REAL NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_session(self, distance: float, timestamp: datetime = None) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if timestamp is None:
            timestamp = datetime.now()
            
        cursor.execute(
            "INSERT INTO exercise_sessions (distance, timestamp) VALUES (?, ?)",
            (distance, timestamp)
        )
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def delete_session(self, session_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM exercise_sessions WHERE id = ?", (session_id,))
        
        conn.commit()
        conn.close()
    
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
    
    def get_today_sessions(self) -> List[ExerciseRecord]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = date.today()
        cursor.execute('''
            SELECT id, distance, timestamp FROM exercise_sessions 
            WHERE date(timestamp) = ?
            ORDER BY timestamp
        ''', (today,))
        
        records = []
        for row in cursor.fetchall():
            records.append(ExerciseRecord(row[0], row[1], datetime.fromisoformat(row[2])))
            
        conn.close()
        return records
    
    def get_daily_totals(self) -> List[Tuple[str, float]]:
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
    
    def get_monthly_totals(self) -> List[Tuple[str, float]]:
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
    
    def get_total_distance(self) -> float:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(distance) FROM exercise_sessions")
        total = cursor.fetchone()[0]
        conn.close()
        
        return total if total else 0.0
    
    def get_today_total(self) -> float:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = date.today()
        cursor.execute('''
            SELECT SUM(distance) FROM exercise_sessions 
            WHERE date(timestamp) = ?
        ''', (today,))
        
        total = cursor.fetchone()[0]
        conn.close()
        
        return total if total else 0.0
    
    def update_session_distance(self, session_id: int, distance: float):
        """Update distance for an existing session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE exercise_sessions SET distance = ? WHERE id = ?", (distance, session_id))
        
        conn.commit()
        conn.close()
    
    def update_session(self, session_id: int, distance: float, timestamp: str):
        """Update both distance and timestamp for an existing session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE exercise_sessions SET distance = ?, timestamp = ? WHERE id = ?", (distance, timestamp, session_id))
        
        conn.commit()
        conn.close()
    
    def get_session_distances(self) -> List[tuple]:
        """Get session distances with timestamps for trend analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, distance, timestamp FROM exercise_sessions 
            ORDER BY timestamp
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_weekly_totals(self) -> List[tuple]:
        """Get weekly total distances"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT strftime('%Y-W%W', timestamp) as week, SUM(distance) as total_distance
            FROM exercise_sessions 
            GROUP BY strftime('%Y-W%W', timestamp)
            ORDER BY week
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_last_session(self) -> ExerciseRecord:
        """Get the most recently added session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, distance, timestamp FROM exercise_sessions ORDER BY timestamp DESC LIMIT 1"
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return ExerciseRecord(row[0], row[1], row[2])
        return None

    def clear_all_data(self):
        """Clear all exercise session data from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM exercise_sessions")
        
        conn.commit()
        conn.close()