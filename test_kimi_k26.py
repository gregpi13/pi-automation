#!/usr/bin/env python3
"""
Test script for Kimi K2.6
Fetches weather data from Open-Meteo API with proper error handling and validation.
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class WeatherError(Exception):
    """Base exception for weather fetch operations."""
    pass


class APIConnectionError(WeatherError):
    """Failed to connect to weather API."""
    pass


class DataValidationError(WeatherError):
    """Weather data failed validation."""
    pass


@dataclass
class WeatherData:
    """Structured weather data container."""
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    condition: str
    location: str
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "condition": self.condition,
            "location": self.location,
            "timestamp": self.timestamp
        }
    
    def __str__(self) -> str:
        """Human-readable weather summary."""
        return (f"{self.location}: {self.temperature}°C (feels like {self.feels_like}°C), "
                f"{self.condition}, humidity {self.humidity}%, wind {self.wind_speed} km/h")


class WeatherFetcher:
    """Fetch and parse weather data from Open-Meteo API."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # WMO Weather interpretation codes
    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail"
    }
    
    def __init__(self, latitude: float, longitude: float, location_name: str = "Unknown"):
        self.latitude = latitude
        self.longitude = longitude
        self.location_name = location_name
    
    def _build_url(self) -> str:
        """Construct API URL with parameters."""
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", 
                       "weather_code", "wind_speed_10m"],
            "timezone": "auto"
        }
        
        # Build query string
        query_parts = []
        for key, value in params.items():
            if isinstance(value, list):
                for v in value:
                    query_parts.append(f"{key}={v}")
            else:
                query_parts.append(f"{key}={value}")
        
        return f"{self.BASE_URL}?{'&'.join(query_parts)}"
    
    def _fetch_raw_data(self) -> Dict[str, Any]:
        """Fetch raw data from API with error handling."""
        url = self._build_url()
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise APIConnectionError("Request timed out after 10 seconds")
        except requests.exceptions.ConnectionError:
            raise APIConnectionError("Failed to connect to Open-Meteo API")
        except requests.exceptions.HTTPError as e:
            raise APIConnectionError(f"HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise APIConnectionError(f"Request failed: {str(e)}")
    
    def _validate_response(self, data: Dict[str, Any]) -> None:
        """Validate API response structure."""
        required_fields = ["current", "latitude", "longitude"]
        
        for field in required_fields:
            if field not in data:
                raise DataValidationError(f"Missing required field: {field}")
        
        current = data.get("current", {})
        required_current = ["temperature_2m", "relative_humidity_2m", 
                           "apparent_temperature", "weather_code", "wind_speed_10m"]
        
        for field in required_current:
            if field not in current:
                raise DataValidationError(f"Missing current weather field: {field}")
            
            # Validate numeric fields
            if field != "weather_code":
                try:
                    float(current[field])
                except (ValueError, TypeError):
                    raise DataValidationError(f"Invalid numeric value for {field}: {current[field]}")
    
    def _parse_weather_code(self, code: int) -> str:
        """Convert WMO weather code to human-readable condition."""
        return self.WEATHER_CODES.get(code, f"Unknown (code {code})")
    
    def fetch(self) -> WeatherData:
        """Fetch and return structured weather data."""
        # Fetch and validate
        raw_data = self._fetch_raw_data()
        self._validate_response(raw_data)
        
        # Parse current conditions
        current = raw_data["current"]
        
        return WeatherData(
            temperature=float(current["temperature_2m"]),
            feels_like=float(current["apparent_temperature"]),
            humidity=int(current["relative_humidity_2m"]),
            wind_speed=float(current["wind_speed_10m"]),
            condition=self._parse_weather_code(current["weather_code"]),
            location=self.location_name,
            timestamp=datetime.now().isoformat()
        )


def main():
    """Main execution - test weather fetch for Caledon, Ontario."""
    print("=" * 60)
    print("Kimi K2.6 Test: Weather Fetcher")
    print("=" * 60)
    
    # Caledon, Ontario coordinates
    fetcher = WeatherFetcher(
        latitude=43.8639,
        longitude=-79.8744,
        location_name="Caledon, Ontario"
    )
    
    try:
        print(f"\nFetching weather for {fetcher.location_name}...")
        weather = fetcher.fetch()
        
        print(f"\n✅ Success!")
        print(f"\n{weather}")
        
        # Output structured JSON
        print(f"\n📊 JSON Output:")
        print(json.dumps(weather.to_dict(), indent=2))
        
        return 0
        
    except APIConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        return 1
    except DataValidationError as e:
        print(f"\n❌ Validation Error: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected Error: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
