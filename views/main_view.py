import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import pandas as pd

class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Exercise Tracker")
        self.root.geometry("1000x700")
        
        # Configure styles with modern blue theme
        style = ttk.Style()
        style.theme_use('clam')  # Use a more modern theme
        
        # Set deep blue background for root window 
        self.root.configure(bg='#1a1a2e')
        # Configure style for frames to use consistent blue theme
        style.configure('Dark.TFrame', background='#1a1a2e')
        style.configure('TLabelframe', background='#16213e', foreground='#4cc9f0', bordercolor='#0f3460')
        style.configure('Modern.TButton', background='#0f3460', foreground='#4cc9f0', bordercolor='#0f3460')
        # Remove problematic font specification to avoid Tcl errors
        
        # Create main content area with better layout hierarchy
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create input frame with enhanced spacing and modern styling - fixed size
        self.input_frame = ttk.Frame(main_frame, style='Dark.TFrame') 
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Make sure input frame doesn't expand beyond its content
        self.input_frame.pack_propagate(False)
        # Set explicit height to accommodate controls properly
        self.input_frame.configure(height=60)
        
        # Enhanced control layout with better visual separation
        ttk.Label(self.input_frame, text="Distance (metres):", foreground='#4cc9f0', background='#16213e').pack(side=tk.LEFT, padx=(10, 5))
        self.distance_entry = ttk.Entry(self.input_frame, width=12)
        self.distance_entry.pack(side=tk.LEFT, padx=5)
        
        # Organized button section with consistent spacing
        button_frame = ttk.Frame(self.input_frame, style='Dark.TFrame')
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        # Add buttons with clean, modern appearance
        self.add_button = ttk.Button(button_frame, text="➕ Add Session", style='Modern.TButton')
        self.add_button.pack(side=tk.LEFT, padx=3)
        
        self.delete_button = ttk.Button(button_frame, text="🗑️ Delete Selected", style='Modern.TButton')  
        self.delete_button.pack(side=tk.LEFT, padx=3)
        
        self.edit_button = ttk.Button(button_frame, text="✎ Edit Selected", style='Modern.TButton')
        self.edit_button.pack(side=tk.LEFT, padx=3)
        
        self.import_button = ttk.Button(button_frame, text="📥 Import Data", style='Modern.TButton')
        self.import_button.pack(side=tk.LEFT, padx=3)
        
        # Create summary frame with rounded corners and modern blue styling - fixed size
        self.summary_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        self.summary_frame.pack(fill=tk.X, padx=10, pady=5)
        # Make sure summary frame doesn't expand beyond its content
        self.summary_frame.pack_propagate(False)
        # Set explicit height to accommodate summary properly - increased size
        self.summary_frame.configure(height=80)
        
        # Add labels to display both total distances
        self.total_distance_label = ttk.Label(self.summary_frame, text="Total Distance: 0.0 metres", foreground='#4cc9f0', background='#16213e')
        self.total_distance_label.pack(pady=(5,0))
        
        self.todays_distance_label = ttk.Label(self.summary_frame, text="Todays Distance: 0.0 metres", foreground='#4cc9f0', background='#16213e')
        self.todays_distance_label.pack(pady=(0,5))
        
        # Create history frame with rounded corners - fixed size  
        self.history_frame = ttk.Frame(main_frame, style='TLabelframe')
        self.history_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)  # Fixed size, no expansion
        # Make sure history frame doesn't expand beyond its content
        self.history_frame.pack_propagate(False)
        # Set explicit height to accommodate treeview properly
        self.history_frame.configure(height=200)
        
        # Add a proper title label that ensures correct coloring (bypasses LabelFrame title issues)
        history_title_label = tk.Label(self.history_frame, text="Session History", foreground='#4cc9f0', background='#16213e', font=('DejaVu Sans', 10, 'bold'))
        history_title_label.pack(anchor='w', padx=10, pady=(5,0))
        
        # Configure treeview styles for modern look
        style.configure('Treeview', 
                       background='#16213e',
                       foreground='#e6e6e6',
                       fieldbackground='#16213e')
        style.map('Treeview', background=[('selected', '#4361ee')])
        style.configure('Treeview.Heading', background='#0f3460', foreground='#4cc9f0')
        
        # Create treeview for history
        columns = ("ID", "Distance", "Timestamp")
        self.history_tree = ttk.Treeview(self.history_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
            
        # Add scrollbar to history
        scrollbar = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create chart frame like a bubble with proper rounding - this should be the only expanding section
        self.chart_frame = ttk.Frame(main_frame, style='TLabelframe')
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add a proper title label that ensures correct coloring (bypasses LabelFrame title issues)
        chart_title_label = tk.Label(self.chart_frame, text="Trend Charts", foreground='#4cc9f0', background='#16213e', font=('DejaVu Sans', 10, 'bold'))
        chart_title_label.pack(anchor='w', padx=10, pady=(5,0))
        
        # Create matplotlib figure with 4 subplots - each in its own row using blue theme
        self.fig = plt.figure(figsize=(15, 28), facecolor='#1a1a2e')  # Increased height slightly
        self.ax1 = self.fig.add_subplot(411)  # Session trends
        self.ax2 = self.fig.add_subplot(412)  # Daily distance
        self.ax3 = self.fig.add_subplot(413)  # Weekly distance
        self.ax4 = self.fig.add_subplot(414)  # Monthly distance
        
        # Set subplot backgrounds to blue for full consistency
        self.ax1.set_facecolor('#16213e')
        self.ax2.set_facecolor('#16213e')  
        self.ax3.set_facecolor('#16213e')
        self.ax4.set_facecolor('#16213e')
        
        # Apply consistent styling to all axes for better visual harmony
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.spines['bottom'].set_color('#0f3460')
            ax.spines['left'].set_color('#0f3460')
            ax.spines['top'].set_color('#0f3460')  
            ax.spines['right'].set_color('#0f3460')
            ax.tick_params(axis='x', colors='#e6e6e6', labelsize=10)
            ax.tick_params(axis='y', colors='#e6e6e6', labelsize=10)
        
        # Adjust subplot layout to give more room for x-axis labels and prevent overlap
        plt.subplots_adjust(top=0.95, bottom=0.18, hspace=0.5)  # Increased bottom margin and reduced top margin
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure the style for plots with professional blue color scheme and enhanced readability
        plt.rcParams['figure.facecolor'] = '#1a1a2e'  # Deep blue background 
        plt.rcParams['axes.facecolor'] = '#16213e'    # Slightly lighter blue for subplot background
        plt.rcParams['axes.edgecolor'] = '#0f3460'   # Dark blue axis edges
        plt.rcParams['axes.labelcolor'] = '#e6e6e6'  # Light gray axis labels for better readability
        plt.rcParams['xtick.color'] = '#e6e6e6'      # Light gray x-tick labels
        plt.rcParams['ytick.color'] = '#e6e6e6'      # Light gray y-tick labels
        plt.rcParams['text.color'] = '#4cc9f0'       # Sky blue text for titles and other elements
        plt.rcParams['font.size'] = 12               # Slightly larger font for readability
        plt.rcParams['axes.linewidth'] = 1.5         # Slightly thicker axis lines for clean look
        
        # Add a professional title with enhanced styling and adjusted position
        self.fig.suptitle('Exercise Progress Trends', fontsize=18, color='#4cc9f0', fontweight='bold', fontfamily='DejaVu Sans')
        
        # Adjust subplot layout to give more room for x-axis labels and prevent overlap
        plt.subplots_adjust(top=0.93, bottom=0.15, hspace=0.4)  # Increased bottom margin and reduced top margin
        
        # Bind events
        self.add_button.config(command=self.on_add_button_click)
        self.delete_button.config(command=self.on_delete_button_click)
        self.edit_button.config(command=self.on_edit_button_click)
        self.import_button.config(command=self.on_import_button_click)
        self.distance_entry.bind('<Return>', lambda e: self.on_add_button_click())
        
        # Initialize charts
        self.update_all()
        
    def on_add_button_click(self):
        try:
            distance = float(self.distance_entry.get())
            if distance <= 0:
                messagebox.showerror("Error", "Distance must be greater than 0")
                return
            
            self.controller.add_session(distance)
            self.distance_entry.delete(0, tk.END)
            self.update_all()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid distance")
    
    def on_delete_button_click(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a session to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this session?"):
            item = selected[0]
            session_id = self.history_tree.item(item)['values'][0]
            self.controller.delete_session(session_id)
            self.update_all()
    
    def on_edit_button_click(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a session to edit")
            return
            
        item = selected[0]
        session_id = self.history_tree.item(item)['values'][0]
        current_distance = self.history_tree.item(item)['values'][1]
        current_timestamp = self.history_tree.item(item)['values'][2]
        
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Session")
        edit_window.geometry("300x200")
        edit_window.configure(bg='#16213e')
        
        # Distance input
        ttk.Label(edit_window, text="Distance (metres):", foreground='#4cc9f0', background='#16213e').pack(pady=5)
        distance_entry = ttk.Entry(edit_window, width=20)
        distance_entry.pack(pady=5)
        distance_entry.insert(0, current_distance)
        
        # Date input
        ttk.Label(edit_window, text="Date & Time:", foreground='#4cc9f0', background='#16213e').pack(pady=5)
        date_entry = ttk.Entry(edit_window, width=20)
        date_entry.pack(pady=5)
        date_entry.insert(0, current_timestamp)
        
        def save_changes():
            try:
                new_distance = float(distance_entry.get())
                if new_distance <= 0:
                    messagebox.showerror("Error", "Distance must be greater than 0")
                    return
                
                # Update the session with both distance and timestamp
                self.controller.edit_session(session_id, new_distance, date_entry.get())
                edit_window.destroy()
                self.update_all()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid distance")
        
        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack(pady=10)
    
    def on_import_button_click(self):
        """Handle import button click"""
        try:
            # Ask user to select a file
            file_path = tk.filedialog.askopenfilename(
                title="Select Historic Data File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not file_path:
                return  # User cancelled
            
            # Import the data
            imported_count = self.controller.import_from_text_file(file_path)
            
            # Show result
            messagebox.showinfo("Import Complete", f"Successfully imported {imported_count} exercise sessions")
            
            # Refresh the display
            self.update_all()
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import data: {str(e)}")
    
    def update_summary(self, total_distance: float, todays_distance: float):
        self.total_distance_label.config(text=f"Total Distance: {total_distance:.2f} metres")
        self.todays_distance_label.config(text=f"Todays Distance: {todays_distance:.2f} metres")
    
    def update_history(self, sessions):
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Add new items
        for session in sessions:
            self.history_tree.insert("", tk.END, values=(
                session.id,
                f"{session.distance:.2f}",
                session.timestamp.strftime("%Y-%m-%d %H:%M")
            ))
    def update_charts(self, session_data=None, daily_data=None, weekly_data=None, monthly_data=None):
        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        
        # Style the subplots with professional blue background
        self.ax1.set_facecolor('#16213e')  # Slightly lighter blue background for subplot
        self.ax2.set_facecolor('#16213e')  # Slightly lighter blue background for subplot
        self.ax3.set_facecolor('#16213e')  # Slightly lighter blue background for subplot
        self.ax4.set_facecolor('#16213e')  # Slightly lighter blue background for subplot
        
        # Set common styling for all axes in the figure with professional color scheme
        self.ax1.spines['bottom'].set_color('#0f3460')
        self.ax1.spines['top'].set_color('#0f3460') 
        self.ax1.spines['left'].set_color('#0f3460')
        self.ax1.spines['right'].set_color('#0f3460')
        
        self.ax2.spines['bottom'].set_color('#0f3460')
        self.ax2.spines['top'].set_color('#0f3460') 
        self.ax2.spines['left'].set_color('#0f3460')
        self.ax2.spines['right'].set_color('#0f3460')
        
        self.ax3.spines['bottom'].set_color('#0f3460')
        self.ax3.spines['top'].set_color('#0f3460') 
        self.ax3.spines['left'].set_color('#0f3460')
        self.ax3.spines['right'].set_color('#0f3460')
        
        self.ax4.spines['bottom'].set_color('#0f3460')
        self.ax4.spines['top'].set_color('#0f3460') 
        self.ax4.spines['left'].set_color('#0f3460')
        self.ax4.spines['right'].set_color('#0f3460')
        
        if session_data:
            # Plot individual session distances over time - Session trends chart
            timestamps = [datetime.fromisoformat(item[2]) for item in session_data]  # Convert timestamp string to datetime
            distances = [item[1] for item in session_data]  # Distance values
            
            # Filter out any None or invalid values
            valid_data = [(t, d) for t, d in zip(timestamps, distances) if d is not None and not pd.isna(d)]
            if valid_data:
                valid_timestamps, valid_distances = zip(*valid_data)
                # Enhanced line chart styling with more professional look using vibrant colors
                self.ax1.plot(valid_timestamps, valid_distances, marker='o', linestyle='-', linewidth=3, markersize=8, color='#4cc9f0', alpha=0.8)
                
                # Add area under the curve for better data visualization
                self.ax1.fill_between(valid_timestamps, valid_distances, alpha=0.2, color='#4cc9f0')
                
                # Position title vertically on the left side of the chart
                self.ax1.text(-0.15, 0.5, 'Session', transform=self.ax1.transAxes, 
                            rotation=90, va='center', ha='center', fontsize=16, color='#4cc9f0')
                
                self.ax1.set_xlabel("Time", color='#e6e6e6', fontsize=12)  # Changed to light gray for readability
                self.ax1.set_ylabel("Distance (metres)", color='#e6e6e6', fontsize=12)  # Changed to light gray for readability
                self.ax1.tick_params(axis='x', rotation=45, colors='#e6e6e6', labelsize=10)
                self.ax1.tick_params(axis='y', colors='#e6e6e6', labelsize=10)
                self.ax1.grid(True, alpha=0.3, color='#0f3460', linestyle='-', linewidth=0.5)
                self.ax1.set_ylim(0, max(valid_distances) * 1.1)  # Add some padding on top
                
                # Ensure legend is visible on dark background
                self.ax1.legend(loc='upper left', frameon=True, facecolor='#16213e', edgecolor='#0f3460', labelcolor='#4cc9f0')
            
        if daily_data:
            dates = [item[0] for item in daily_data]
            distances = [item[1] for item in daily_data]
            
            # Enhanced bar chart styling with vibrant colors and 3D-like look
            bars = self.ax2.bar(range(len(dates)), distances, color='#f72585', alpha=0.8, edgecolor='#4361ee', linewidth=1)
            
            # Position title vertically on the left side of the chart
            self.ax2.text(-0.15, 0.5, 'Daily', transform=self.ax2.transAxes, 
                        rotation=90, va='center', ha='center', fontsize=16, color='#4cc9f0')
            
            self.ax2.set_xlabel("Date", color='#e6e6e6', fontsize=12)  # Changed to light gray for readability
            # Remove y-label for second chart to save space
            self.ax2.tick_params(axis='x', rotation=45, colors='#e6e6e6', labelsize=10)
            self.ax2.tick_params(axis='y', colors='#e6e6e6', labelsize=10)
            self.ax2.grid(True, alpha=0.3, color='#0f3460', linestyle='-', linewidth=0.5)
            
            # Enhanced data labels for better clarity with improved styling
            for i, (date, dist) in enumerate(zip(dates, distances)):
                self.ax2.annotate(f'{dist:.0f}m', (i, dist), textcoords="offset points", xytext=(0,10), ha='center', 
                                fontsize=10, color='#4cc9f0', fontweight='bold')
            
            # Set y-axis to start from 0 for better comparison
            max_dist = max(distances) if distances else 1
            self.ax2.set_ylim(0, max_dist * 1.1)
            
            # Ensure legend is visible on dark background
            self.ax2.legend(loc='upper left', frameon=True, facecolor='#16213e', edgecolor='#0f3460', labelcolor='#4cc9f0')
            
        if weekly_data:
            weeks = [item[0] for item in weekly_data]
            distances = [item[1] for item in weekly_data]
            
            # Enhanced bar chart with gradient-like appearance and vibrant colors
            bars = self.ax3.bar(range(len(weeks)), distances, color='#4361ee', alpha=0.8, edgecolor='#4cc9f0', linewidth=1)
            
            # Position title vertically on the left side of the chart
            self.ax3.text(-0.15, 0.5, 'Weekly', transform=self.ax3.transAxes, 
                        rotation=90, va='center', ha='center', fontsize=16, color='#4cc9f0')
            
            self.ax3.set_xlabel("Week", color='#e6e6e6', fontsize=12)  # Changed to light gray for readability
            # Remove y-label for third chart to save space
            self.ax3.set_xticks(range(len(weeks)))
            self.ax3.set_xticklabels(weeks, rotation=45, color='#e6e6e6', fontsize=10)
            self.ax3.tick_params(axis='y', colors='#e6e6e6', labelsize=10)
            self.ax3.grid(True, alpha=0.3, color='#0f3460', linestyle='-', linewidth=0.5)
            
            # Enhanced value labels on bars for clarity
            max_dist = max(distances) if distances else 1
            for i, (week, dist) in enumerate(zip(weeks, distances)):
                self.ax3.text(i, dist + max_dist * 0.02, f'{dist:.0f}m', ha='center', va='bottom', 
                            fontsize=10, color='#4cc9f0', fontweight='bold')
            
            # Set y-axis to start from 0 for better comparison
            self.ax3.set_ylim(0, max_dist * 1.1)
            
            # Ensure legend is visible on dark background
            self.ax3.legend(loc='upper left', frameon=True, facecolor='#16213e', edgecolor='#0f3460', labelcolor='#4cc9f0')
            
        if monthly_data:
            months = [item[0] for item in monthly_data]
            distances = [item[1] for item in monthly_data]
            
            # Convert month-year format to named months
            month_names = []
            for month in months:
                try:
                    # Parse the month-year string (format: YYYY-MM)
                    month_obj = datetime.strptime(month, '%Y-%m')
                    month_name = month_obj.strftime('%b')  # Abbreviated month name (Jan, Feb, etc)
                    year = month_obj.strftime('%Y')
                    month_names.append(f"{month_name}\n{year}")
                except ValueError:
                    # If parsing fails, keep original
                    month_names.append(month)
            
            # Enhanced bar chart with rich color scheme and visual effects
            bars = self.ax4.bar(range(len(months)), distances, color='#7209b7', alpha=0.8, edgecolor='#f72585', linewidth=1)
            
            # Position title vertically on the left side of the chart
            self.ax4.text(-0.15, 0.5, 'Monthly', transform=self.ax4.transAxes, 
                        rotation=90, va='center', ha='center', fontsize=16, color='#4cc9f0')
            
            self.ax4.set_xlabel("Month", color='#e6e6e6', fontsize=12)  # Changed to light gray for readability
            # Remove y-label for fourth chart to save space
            self.ax4.set_xticks(range(len(months)))
            self.ax4.set_xticklabels(month_names, rotation=45, color='#e6e6e6', fontsize=10)
            self.ax4.tick_params(axis='y', colors='#e6e6e6', labelsize=10)
            self.ax4.grid(True, alpha=0.3, color='#0f3460', linestyle='-', linewidth=0.5)
            
            # Enhanced value labels on bars for clarity
            max_dist = max(distances) if distances else 1
            for i, (month, dist) in enumerate(zip(month_names, distances)):
                self.ax4.text(i, dist + max_dist * 0.02, f'{dist:.0f}m', ha='center', va='bottom', 
                            fontsize=10, color='#4cc9f0', fontweight='bold')
            
            # Set y-axis to start from 0 for better comparison
            self.ax4.set_ylim(0, max_dist * 1.1)
            
            # Ensure legend is visible on dark background
            self.ax4.legend(loc='upper left', frameon=True, facecolor='#16213e', edgecolor='#0f3460', labelcolor='#4cc9f0')
        
        # Add a common title for the figure with enhanced styling
        self.fig.suptitle('Exercise Progress Trends', fontsize=18, color='#4cc9f0', fontweight='bold', fontfamily='DejaVu Sans')
        plt.subplots_adjust(top=0.95)  # Make room for the title and reduce spacing
        
        self.canvas.draw()
    
    def update_all(self):
        # Called when data is updated
        total_distance = self.controller.get_total_distance()
        todays_distance = self.controller.get_today_total()
        sessions = self.controller.get_all_sessions()
        daily_data = self.controller.get_daily_totals()
        monthly_data = self.controller.get_monthly_totals()
        session_data = self.controller.get_session_distances()
        weekly_data = self.controller.get_weekly_totals()
        
        self.update_summary(total_distance, todays_distance)
        self.update_history(sessions)
        self.update_charts(session_data, daily_data, weekly_data, monthly_data)
        
    def show(self):
        self.root.mainloop()