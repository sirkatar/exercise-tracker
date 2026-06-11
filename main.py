import sys
import os
from tkinter import Tk
from views.main_view import MainView
from controllers.exercise_controller import ExerciseController
from services.database_service import DatabaseService

def main():
    # Initialize database service
    db_service = DatabaseService()
    
    # Initialize controller
    controller = ExerciseController(db_service)
    
    # Initialize view
    view = MainView(controller)
    
    # Show the application
    view.show()

if __name__ == "__main__":
    main()