#!/usr/bin/env python3
"""
Great Circle Distance Calculator using the Haversine formula.

This tool calculates the distance between two points on Earth's surface
given their latitude and longitude coordinates.
"""

from math import radians, cos, sin, asin, sqrt, degrees
from typing import Tuple, Dict, List
from dataclasses import dataclass


class ValidationError(Exception):
    """Custom exception for coordinate validation errors."""
    pass


@dataclass
class Coordinate:
    """Represents a geographic coordinate with latitude and longitude."""
    latitude: float
    longitude: float
    
    def __post_init__(self):
        """Validate coordinates after initialization."""
        if not -90 <= self.latitude <= 90:
            raise ValidationError(
                f"Latitude {self.latitude} is invalid. Must be between -90 and 90."
            )
        if not -180 <= self.longitude <= 180:
            raise ValidationError(
                f"Longitude {self.longitude} is invalid. Must be between -180 and 180."
            )
    
    def to_radians(self) -> Tuple[float, float]:
        """Convert coordinates to radians."""
        return radians(self.latitude), radians(self.longitude)


def get_coordinate(location_type: str) -> Coordinate:
    """
    Prompt user for latitude and longitude coordinates.
    
    Args:
        location_type: Either "origin" or "destination"
    
    Returns:
        Coordinate object with validated lat/lon
    
    Raises:
        ValidationError: If coordinates are out of valid range
    """
    print(f"\n{location_type.upper()} COORDINATES")
    print("-" * 40)
    
    while True:
        try:
            lat = float(input(f"Enter {location_type} latitude (decimal degrees): "))
            lon = float(input(f"Enter {location_type} longitude (decimal degrees): "))
            return Coordinate(lat, lon)
        except ValueError:
            print("❌ Please enter valid numeric values.\n")
        except ValidationError as e:
            print(f"❌ {e}\n")


def haversine_distance(origin: Coordinate, destination: Coordinate) -> Dict[str, float]:
    """
    Calculate the great circle distance between two points using the Haversine formula.
    
    Args:
        origin: Starting coordinate
        destination: Ending coordinate
    
    Returns:
        Dictionary containing distances in kilometers, statute miles, and nautical miles
    """
    # Convert to radians
    origin_lat_rad, origin_lon_rad = origin.to_radians()
    dest_lat_rad, dest_lon_rad = destination.to_radians()
    
    # Haversine formula
    dlon = dest_lon_rad - origin_lon_rad
    dlat = dest_lat_rad - origin_lat_rad
    
    a = sin(dlat / 2) ** 2 + cos(origin_lat_rad) * cos(dest_lat_rad) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    
    # Earth's radius in different units
    radius_km = 6371.0
    radius_statute_miles = 3959.0  # More accurate than 3596.0
    radius_nautical_miles = 3440.1
    
    return {
        'kilometers': round(c * radius_km, 3),
        'statute_miles': round(c * radius_statute_miles, 3),
        'nautical_miles': round(c * radius_nautical_miles, 3)
    }


def calculate_initial_bearing(origin: Coordinate, destination: Coordinate) -> float:
    """
    Calculate the initial bearing (forward azimuth) from origin to destination.
    
    Args:
        origin: Starting coordinate
        destination: Ending coordinate
    
    Returns:
        Initial bearing in degrees (0-360)
    """
    origin_lat_rad, origin_lon_rad = origin.to_radians()
    dest_lat_rad, dest_lon_rad = destination.to_radians()
    
    dlon = dest_lon_rad - origin_lon_rad
    
    x = sin(dlon) * cos(dest_lat_rad)
    y = cos(origin_lat_rad) * sin(dest_lat_rad) - sin(origin_lat_rad) * cos(dest_lat_rad) * cos(dlon)
    
    initial_bearing = degrees(asin(x / sqrt(x**2 + y**2)))
    
    # Normalize to 0-360 degrees
    bearing = (degrees(asin(x / sqrt(x**2 + y**2))) + 360) % 360
    
    # More accurate calculation
    bearing = degrees(asin(x / sqrt(x**2 + y**2)))
    bearing = (bearing + 360) % 360
    
    # Using atan2 for more accurate bearing
    from math import atan2
    bearing = atan2(x, y)
    bearing = (degrees(bearing) + 360) % 360
    
    return round(bearing, 1)


def format_coordinate(coord: Coordinate) -> str:
    """Format a coordinate as a readable string."""
    lat_dir = "N" if coord.latitude >= 0 else "S"
    lon_dir = "E" if coord.longitude >= 0 else "W"
    return f"{abs(coord.latitude):.3f}°{lat_dir}, {abs(coord.longitude):.3f}°{lon_dir}"


def display_results(origin: Coordinate, destination: Coordinate, distances: Dict[str, float], bearing: float):
    """Display calculation results in a formatted table."""
    print("\n" + "=" * 70)
    print("GREAT CIRCLE DISTANCE CALCULATION RESULTS")
    print("=" * 70)
    
    print(f"\nOrigin:      {format_coordinate(origin)}")
    print(f"Destination: {format_coordinate(destination)}")
    print(f"\nInitial Bearing: {bearing}° (from origin to destination)")
    
    print("\n" + "-" * 70)
    print(f"{'UNIT':<25} {'DISTANCE':>15}")
    print("-" * 70)
    print(f"{'Kilometers':<25} {distances['kilometers']:>15,.3f} km")
    print(f"{'Statute Miles':<25} {distances['statute_miles']:>15,.3f} mi")
    print(f"{'Nautical Miles':<25} {distances['nautical_miles']:>15,.3f} NM")
    print("-" * 70)


def main():
    """Main program loop."""
    print("=" * 70)
    print("GREAT CIRCLE DISTANCE CALCULATOR")
    print("=" * 70)
    print("\nThis tool calculates the shortest distance between two points")
    print("on Earth's surface using the Haversine formula.")
    print("\nCoordinates should be entered in decimal degrees:")
    print("  • Latitude: -90 to 90 (negative = South)")
    print("  • Longitude: -180 to 180 (negative = West)")
    
    while True:
        try:
            # Get coordinates
            origin = get_coordinate("origin")
            destination = get_coordinate("destination")
            
            # Calculate distances and bearing
            distances = haversine_distance(origin, destination)
            bearing = calculate_initial_bearing(origin, destination)
            
            # Display results
            display_results(origin, destination, distances, bearing)
            
            # Ask to calculate again
            again = input("\n\nCalculate another route? (y/n): ").lower().strip()
            if again != 'y':
                print("\nThank you for using the Great Circle Distance Calculator!")
                break
            print("\n" + "=" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()