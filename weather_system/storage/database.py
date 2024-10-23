from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from weather_system.config.settings import Settings
from weather_system.models.weather_data import WeatherData

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = 'weather_records'
    
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    city_id = Column(String)
    temperature = Column(Float)
    feels_like = Column(Float)
    weather_condition = Column(String)
    timestamp = Column(DateTime)

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(Settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_weather_data(self, weather_data: 'WeatherData'):
        session = self.Session()
        record = WeatherRecord(
            city_name=weather_data.city_name,
            city_id=weather_data.city_id,
            temperature=weather_data.temperature,
            feels_like=weather_data.feels_like,
            weather_condition=weather_data.weather_condition,
            timestamp=weather_data.timestamp
        )
        session.add(record)
        session.commit()
        session.close()