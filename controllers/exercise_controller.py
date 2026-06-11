from typing import List
from models.exercise_model import ExerciseRecord
from services.database_service import DatabaseService
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class ExerciseController:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    def add_session(self, distance: float) -> int:
        """Add a new exercise session"""
        return self.db_service.insert_session(distance)
    
    def edit_session(self, session_id: int, distance: float, timestamp: str = None):
        """Edit an existing exercise session"""
        if timestamp:
            self.db_service.update_session(session_id, distance, timestamp)
        else:
            self.db_service.update_session_distance(session_id, distance)
    
    def delete_session(self, session_id: int):
        """Delete an exercise session"""
        self.db_service.delete_session(session_id)
    
    def import_from_text_file(self, file_path: str) -> int:
        """Import exercise data from a text file with format: Date	time	distance (m)"""
        try:
            imported_count = 0
            
            with open(file_path, 'r') as file:
                # Skip header line if it exists
                header_line = file.readline().strip()
                if header_line == "Date\ttime\tdistance (m)":
                    # Header found, skip it and continue
                    pass
                
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        date_str = parts[0]
                        time_str = parts[1]
                        distance_str = parts[2]
                        
                        try:
                            # Parse date and time
                            datetime_str = f"{date_str} {time_str}"
                            timestamp = datetime.strptime(datetime_str, "%d/%m/%y %H:%M:%S")
                            
                            # Parse distance
                            distance = float(distance_str)
                            
                            # Insert into database using existing method
                            self.db_service.insert_session(distance, timestamp)
                            imported_count += 1
                            
                        except ValueError as e:
                            print(f"Skipping invalid line: {line}")
                            continue
            
            return imported_count
            
        except Exception as e:
            raise Exception(f"Error importing data: {str(e)}")
    
    def get_weekly_totals(self) -> List[tuple]:
        """Get weekly total distances"""
        return self.db_service.get_weekly_totals()
    
    def get_all_sessions(self) -> List[ExerciseRecord]:
        """Get all exercise sessions"""
        return self.db_service.get_all_sessions()
    
    def get_daily_totals(self) -> List[tuple]:
        """Get daily total distances"""
        return self.db_service.get_daily_totals()
    
    def get_monthly_totals(self) -> List[tuple]:
        """Get monthly total distances"""
        return self.db_service.get_monthly_totals()
    
    def get_session_distances(self) -> List[tuple]:
        """Get session distances with timestamps for trend analysis"""
        return self.db_service.get_session_distances()
    
    def get_total_distance(self) -> float:
        """Get total distance across all sessions"""
        return self.db_service.get_total_distance()
    
    def get_today_total(self) -> float:
        """Get today's total distance"""
        return self.db_service.get_today_total()
    
    def get_today_sessions(self) -> List[ExerciseRecord]:
        """Get today's exercise sessions"""
        return self.db_service.get_today_sessions()