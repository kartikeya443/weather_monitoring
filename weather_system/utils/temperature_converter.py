class TemperatureConverter:
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        return kelvin - 273.15
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        return (celsius * 9/5) + 32