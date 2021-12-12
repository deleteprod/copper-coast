#!/usr/bin/env python3

import math
import re
import time

def check_rwy_heading():
    runway_heading = input("Please give the departure runway number in two digit format: ")
    # Runway heading sanitising
    runway_heading = re.sub("[^0-9]", "", runway_heading)
    if int(runway_heading) > 36:
        runway_heading = str(round(int(runway_heading)/10)*10)
    runway_heading = runway_heading[:2]
    num_runway = int(runway_heading)
    
    if num_runway < 1 or num_runway > 36:
        print("You gave runway number {}".format(str(runway_heading)))
        print("This is an invalid runway number. Please check and try again.\n")
        time.sleep(5)
        check_rwy_heading()
    else:
        print("\nYou gave runway number {}\n".format(str(runway_heading)))
    return runway_heading
    
def check_wind_dir():
    wind_direction = input("Please give the wind direction as a three digit value: ")
    # Wind direction sanitising
    wind_direction_length = int(len(wind_direction))
    wind_direction = int(wind_direction)
    if not wind_direction_length == 3 or wind_direction > 360 or wind_direction < 1:
        print("You gave wind direction of {}".format(str(wind_direction)))
        print("This is an invalid value. Please check and try again.\n")
        time.sleep(5)
        check_wind_dir()
    else:
        print("\nYou gave wind direction of {}\n".format(str(wind_direction)))
    return wind_direction
        
def check_wind_speed():
    wind_speed_kts = input("Please give the wind speed as a two digit value in knots: ")
    # Wind speed sanitising
    wind_speed_kts = int(wind_speed_kts)
    if wind_speed_kts < 0 or wind_speed_kts > 50:
        print("You gave wind speed of {} knots\n".format(str(wind_speed_kts)))
        print("This is an invalid value. Valid values are between 0 and 50.\n")
        time.sleep(5)
        check_wind_speed()
    else:
        print("\nYou gave a wind speed of {} knots\n".format(str(wind_speed_kts)))
        return wind_speed_kts
    
def calculate_crosswind(runway_heading,wind_direction,wind_speed_kts):
    #print("Made it to the crosswind calculator")
    runway_heading=10*(int(runway_heading))
    tailwind_warning_check = math.fabs(runway_heading - wind_direction)
    if tailwind_warning_check < -90 or tailwind_warning_check > 90:
        print("CAUTION, TAILWIND!!! Tailwind factor: {}".format(str(tailwind_warning_check)))
    crosswind_component = math.sin(math.radians(wind_direction-runway_heading))*wind_speed_kts
    #crosswind_component=round(crosswind_component, 2)
    if crosswind_component > 0 and crosswind_component < 90:
        crosswind_element = "From right to left"
    elif crosswind_component < 0 and crosswind_component > -90:
        crosswind_element = "From left to right"
    elif crosswind_component < -90 or crosswind_component > 90:
        crosswind_element = "CAUTION TAILWIND!!!"
    
    print("Crosswind component = {}".format(str(round(crosswind_component, 2))))
    print("Crosswind element = {}".format(str(crosswind_element)))
    
def main():
    # Prompt user for input and validate
    rwy_heading = check_rwy_heading()
    wind_dir = check_wind_dir()
    wind_speed = check_wind_speed()
    
    # Take validated input and calculate the crosswind
    calculate_crosswind(rwy_heading, wind_dir, wind_speed)
    
main()
    
