import pytest
from datetime import datetime
from weather_system.storage.database import DatabaseManager, WeatherRecord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from weather_system.models.weather_data import WeatherData
from weather_system.storage.database import Base

@pytest.fixture
def db_manager():
    # Use in-memory SQLite for testing
    manager = DatabaseManager()
    manager.engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(manager.engine)
    return manager

def test_save_weather_data(db_manager):
    test_data = WeatherData(
        city_name="Delhi",
        city_id="1273294",
        temperature=27.0,
        feels_like=29.0,
        weather_condition="Clear",
        timestamp=datetime.now()
    )
    
    db_manager.save_weather_data(test_data)
    
    session = db_manager.Session()
    record = session.query(WeatherRecord).first()
    
    assert record is not None
    assert record.city_name == "Delhi"
    assert record.temperature == 27.0
    assert record.weather_condition == "Clear"
    session.close()