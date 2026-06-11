import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

def create_daily_chart(daily_data):
    """Create daily distance chart"""
    if not daily_data:
        return None
        
    dates = [datetime.strptime(item[0], '%Y-%m-%d') for item in daily_data]
    distances = [item[1] for item in daily_data]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, distances, marker='o', linewidth=2, markersize=6)
    ax.set_title('Daily Exercise Distance')
    ax.set_xlabel('Date')
    ax.set_ylabel('Distance (km)')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    return fig

def create_monthly_chart(monthly_data):
    """Create monthly distance chart"""
    if not monthly_data:
        return None
        
    months = [item[0] for item in monthly_data]
    distances = [item[1] for item in monthly_data]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(months, distances, color='skyblue')
    ax.set_title('Monthly Exercise Distance')
    ax.set_xlabel('Month')
    ax.set_ylabel('Distance (km)')
    
    # Add value labels on bars
    for bar, distance in zip(bars, distances):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f'{distance:.1f}', ha='center', va='bottom')
                
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    return fig

def format_date(date_string):
    """Helper function to format date strings"""
    return datetime.strptime(date_string, '%Y-%m-%d').strftime('%B %d, %Y')