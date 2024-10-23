import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict
from weather_system.models.weather_data import WeatherData

class WeatherVisualizer:
    def __init__(self):
        self.plt = plt
        self.plt.style.use('seaborn')

    def plot_daily_temperatures(self, summaries: List[Dict], city: str):
        """Plot daily temperature trends"""
        dates = [summary['date'] for summary in summaries]
        avg_temps = [summary['avg_temperature'] for summary in summaries]
        max_temps = [summary['max_temperature'] for summary in summaries]
        min_temps = [summary['min_temperature'] for summary in summaries]

        plt.figure(figsize=(12, 6))
        plt.plot(dates, avg_temps, 'g-', label='Average Temperature')
        plt.plot(dates, max_temps, 'r-', label='Maximum Temperature')
        plt.plot(dates, min_temps, 'b-', label='Minimum Temperature')
        
        plt.title(f'Daily Temperature Trends - {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        
        return plt

    def plot_weather_conditions(self, summaries: List[Dict], city: str):
        """Plot distribution of weather conditions"""
        condition_counts = {}
        for summary in summaries:
            for condition, count in summary['condition_distribution'].items():
                condition_counts[condition] = condition_counts.get(condition, 0) + count

        plt.figure(figsize=(10, 6))
        plt.bar(condition_counts.keys(), condition_counts.values())
        plt.title(f'Weather Conditions Distribution - {city}')
        plt.xlabel('Weather Condition')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        
        return plt