#!/usr/bin/env python3
"""Crosswind calculator for pilots."""
import math
from typing import Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def get_runway_heading() -> int:
    """
    Prompt for and validate runway heading.
    
    Returns:
        int: Validated runway heading (1-36)
    
    Raises:
        ValidationError: If runway heading is invalid
    """
    runway_input = input("Please give the departure runway number in two digit format: ")
    
    # Remove non-numeric characters
    runway_str = ''.join(c for c in runway_input if c.isdigit())
    
    if not runway_str:
        raise ValidationError("No valid digits provided")
    
    runway_num = int(runway_str)
    
    # Handle numbers > 36 by rounding to nearest 10
    if runway_num > 36:
        runway_num = round(runway_num / 10)
    
    # Take only first two digits
    runway_num = int(str(runway_num)[:2])
    
    if not 1 <= runway_num <= 36:
        raise ValidationError(f"Runway number {runway_num} is invalid. Must be between 1 and 36.")
    
    print(f"\nYou gave runway number {runway_num:02d}\n")
    return runway_num


def get_wind_direction() -> int:
    """
    Prompt for and validate wind direction.
    
    Returns:
        int: Validated wind direction (1-360 degrees)
    
    Raises:
        ValidationError: If wind direction is invalid
    """
    wind_input = input("Please give the wind direction as a three digit value: ")
    
    try:
        wind_dir = int(wind_input)
    except ValueError:
        raise ValidationError(f"Wind direction '{wind_input}' is not a valid number")
    
    if not (1 <= wind_dir <= 360):
        raise ValidationError(f"Wind direction {wind_dir} is invalid. Must be between 1 and 360.")
    
    if len(wind_input.strip()) != 3:
        raise ValidationError(f"Wind direction must be a three digit value (e.g., 270, not {wind_input})")
    
    print(f"\nYou gave wind direction of {wind_dir:03d}\n")
    return wind_dir


def get_wind_speed() -> int:
    """
    Prompt for and validate wind speed.
    
    Returns:
        int: Validated wind speed in knots (0-50)
    
    Raises:
        ValidationError: If wind speed is invalid
    """
    wind_input = input("Please give the wind speed as a two digit value in knots: ")
    
    try:
        wind_speed = int(wind_input)
    except ValueError:
        raise ValidationError(f"Wind speed '{wind_input}' is not a valid number")
    
    if not (0 <= wind_speed <= 50):
        raise ValidationError(f"Wind speed {wind_speed} is invalid. Must be between 0 and 50 knots.")
    
    print(f"\nYou gave a wind speed of {wind_speed} knots\n")
    return wind_speed


def calculate_crosswind(runway_heading: int, wind_direction: int, wind_speed: int) -> dict:
    """
    Calculate crosswind and headwind components.
    
    Args:
        runway_heading: Runway number (1-36)
        wind_direction: Wind direction in degrees (1-360)
        wind_speed: Wind speed in knots
    
    Returns:
        dict: Contains crosswind, headwind, angle, and warnings
    """
    # Convert runway heading to degrees
    runway_deg = runway_heading * 10
    
    # Calculate angle between runway and wind
    angle_diff = wind_direction - runway_deg
    
    # Normalize angle to -180 to 180
    while angle_diff > 180:
        angle_diff -= 360
    while angle_diff < -180:
        angle_diff += 360
    
    # Calculate components
    crosswind = math.sin(math.radians(angle_diff)) * wind_speed
    headwind = math.cos(math.radians(angle_diff)) * wind_speed
    
    # Determine crosswind direction
    if crosswind > 0:
        crosswind_direction = "From right to left"
    elif crosswind < 0:
        crosswind_direction = "From left to right"
    else:
        crosswind_direction = "No crosswind"
    
    # Check for tailwind (headwind component is negative)
    is_tailwind = headwind < 0
    
    return {
        'crosswind': round(abs(crosswind), 2),
        'headwind': round(headwind, 2),
        'crosswind_direction': crosswind_direction,
        'is_tailwind': is_tailwind,
        'angle': round(angle_diff, 1)
    }


def display_results(results: dict) -> None:
    """Display calculation results."""
    if results['is_tailwind']:
        print("⚠️  CAUTION: TAILWIND! ⚠️")
        print(f"Tailwind component: {abs(results['headwind'])} knots\n")
    else:
        print(f"Headwind component: {results['headwind']} knots")
    
    print(f"Crosswind component: {results['crosswind']} knots")
    print(f"Crosswind direction: {results['crosswind_direction']}")
    print(f"Wind angle relative to runway: {results['angle']}°")


def main():
    """Main program loop."""
    print("=== Pilot Crosswind Calculator ===\n")
    
    while True:
        try:
            # Get validated inputs
            runway = get_runway_heading()
            wind_dir = get_wind_direction()
            wind_speed = get_wind_speed()
            
            # Calculate and display results
            results = calculate_crosswind(runway, wind_dir, wind_speed)
            display_results(results)
            
            # Ask if user wants to calculate again
            again = input("\nCalculate another? (y/n): ").lower()
            if again != 'y':
                break
            print("\n" + "="*40 + "\n")
            
        except ValidationError as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.\n")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()