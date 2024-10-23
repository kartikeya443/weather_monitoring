import asyncio
import logging
import signal
from datetime import datetime, timedelta
from typing import Dict, List

from weather_system.core.weather_client import WeatherClient
from weather_system.core.data_processor import DataProcessor, WeatherAggregator
from weather_system.alerts.threshold_manager import ThresholdManager
from weather_system.alerts.notifier import AlertNotifier
from weather_system.storage.database import DatabaseManager
from weather_system.visualization.plotter import WeatherVisualizer
from weather_system.config.settings import Settings
from weather_system.models.weather_data import WeatherData

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WeatherMonitoringSystem:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.weather_client = WeatherClient()
        self.data_processor = DataProcessor()
        self.aggregator = WeatherAggregator()
        self.threshold_manager = ThresholdManager()
        self.notifier = AlertNotifier()
        self.db_manager = DatabaseManager()
        self.visualizer = WeatherVisualizer()
        self.running = True

    async def process_city_weather(self, weather_data: WeatherData):
        """Process weather data for a single city"""
        try:
            # Process and convert temperatures
            processed_data = self.data_processor.process_weather_data(weather_data)
            
            # Store in database
            self.db_manager.save_weather_data(processed_data)
            
            # Add to aggregator for daily summaries
            self.aggregator.add_reading(processed_data)
            
            # Check for threshold violations
            alerts = self.threshold_manager.check_thresholds(processed_data)
            if alerts:
                self.notifier.process_alerts(alerts)
                
        except Exception as e:
            self.logger.error(f"Error processing weather data for {weather_data.city_name}: {str(e)}")

    async def update_weather_data(self):
        """Main loop to fetch and process weather data"""
        while self.running:
            try:
                # Fetch weather data for all cities
                weather_data_list = await self.weather_client.get_weather_for_all_cities()
                
                # Process each city's data
                for weather_data in weather_data_list:
                    await self.process_city_weather(weather_data)
                
                # Generate visualizations periodically (every hour)
                current_minute = datetime.now().minute
                if current_minute == 0:
                    self.generate_visualizations()
                
                # Wait for next update interval
                await asyncio.sleep(Settings.POLLING_INTERVAL)
                
            except Exception as e:
                self.logger.error(f"Error in weather update loop: {str(e)}")
                await asyncio.sleep(60)  # Wait a minute before retrying

    def generate_visualizations(self):
        """Generate and save visualization plots"""
        try:
            for city in Settings.CITIES:
                # Get last 7 days of summaries
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=7)
                
                summaries = []
                current_date = start_date
                while current_date <= end_date:
                    summary = self.aggregator.get_daily_summary(current_date)
                    if summary:
                        summaries.append(summary)
                    current_date += timedelta(days=1)

                if summaries:
                    # Generate and save temperature plot
                    temp_plot = self.visualizer.plot_daily_temperatures(summaries, city['name'])
                    temp_plot.savefig(f"visualizations/{city['name']}_temperatures.png")
                    temp_plot.close()

                    # Generate and save weather conditions plot
                    conditions_plot = self.visualizer.plot_weather_conditions(summaries, city['name'])
                    conditions_plot.savefig(f"visualizations/{city['name']}_conditions.png")
                    conditions_plot.close()

        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")

    def handle_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        self.logger.info("Shutting down weather monitoring system...")
        self.running = False

    def run(self):
        """Start the weather monitoring system"""
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

        # Create event loop and run the main process
        loop = asyncio.get_event_loop()
        try:
            self.logger.info("Starting weather monitoring system...")
            loop.run_until_complete(self.update_weather_data())
        finally:
            loop.close()

if __name__ == "__main__":
    weather_system = WeatherMonitoringSystem()
    weather_system.run()