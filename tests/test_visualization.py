import pytest
from weather_system.visualization.plotter import WeatherVisualizer
import matplotlib.pyplot as plt
from datetime import datetime

def test_plot_generation():
    visualizer = WeatherVisualizer()
    
    test_summaries = [
        {
            'date': datetime.now().date(),
            'avg_temperature': 27.0,
            'max_temperature': 32.0,
            'min_temperature': 22.0,
            'condition_distribution': {'Clear': 10, 'Clouds': 5}
        }
    ]
    
    # Test temperature plot
    temp_plot = visualizer.plot_daily_temperatures(test_summaries, "Delhi")
    assert isinstance(temp_plot, plt.Figure)
    plt.close()
    
    # Test conditions plot
    conditions_plot = visualizer.plot_weather_conditions(test_summaries, "Delhi")
    assert isinstance(conditions_plot, plt.Figure)
    plt.close()