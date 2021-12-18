#!/usr/bin/env python3

'''
Notes TODO:
--------------------------------------
Get initial heading on departure
Get midway heading (with lat and long of midway point) 
Get final heading on arrival

The above calculations are hard though, and will involve a lot of
working things out and substitution of values etc.
'''

from math import radians, cos, sin, asin, sqrt, degrees
from prettytable import PrettyTable

def get_origin_lat():
    # Where are you for latitude?
    while True:
        origin_lat = input("Input the starting latitude in decimal degrees: \n")
        origin_lat = float(origin_lat)
        if origin_lat < -90:
            print("Invalid value for latitude, please try again.")
            continue
        elif origin_lat > 90:
            print("Invalid value for latitude, please try again.")
            continue
        else:
            break
    return origin_lat

def get_origin_lon():
    # Where are you for longitude?
    while True:
        origin_lon = input("Input the origin longitude in decimal degrees: \n")
        origin_lon = float(origin_lon)
        if origin_lon < -180:
            print("Invalid value for longitude, exiting now. Exiting now.")
            continue
        elif float(origin_lon) > 180:
            print("Invalid value for longitude, exiting now. Exiting now.")
            continue
        else:
            break
    return origin_lon

def get_dest_lat():
    # Where are you going to, latitude?
    while True:
        dest_lat = input("Input the starting latitude in decimal degrees: \n")
        dest_lat = float(dest_lat)
        if dest_lat < -90:
            print("Invalid value for latitude, please try again.")
            continue
        elif dest_lat > 90:
            print("Invalid value for latitude, please try again.")
            continue
        else:
            break
    return dest_lat

def get_dest_lon():
    # Where are you going to, longitude?
    while True:
        dest_lon = input("Input the origin longitude in decimal degrees: \n")
        dest_lon = float(dest_lon)
        if dest_lon < -180:
            print("Invalid value for longitude, exiting now. Exiting now.")
            continue
        elif dest_lon > 180:
            print("Invalid value for longitude, exiting now. Exiting now.")
            continue
        else:
            break
    return dest_lon

def haversine(origin_lon, origin_lat, dest_lon, dest_lat, measurement=None):
    
    """
    Use the haversine formula to calculate the great circle
    distance between two points in various units - note this
    requires origin and dest lat/lon in to be specified in 
    decimal degrees.
    """

    # Convert decimal inputs to radians 
    origin_lon, origin_lat, dest_lon, dest_lat = map(radians, [origin_lon, origin_lat, dest_lon, dest_lat])

    # haversine formula 
    dlon = dest_lon - origin_lon 
    dlat = dest_lat - origin_lat 
    a = sin(dlat/2)**2 + cos(origin_lat) * cos(dest_lat) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    print("\nCalculating distance from your origin to your destination...")

    table = PrettyTable()
    loop_counter = 1
    table.field_names = ["Origin Latitude", "Origin Longitude", "Dest Latitude", "Dest Longitude", "Distance", "Unit"]
    for r in [6371.0, 3596.0, 3440.1]:
        if loop_counter == 1:
            unit = "kilometres"
        elif loop_counter == 2:
            unit = "statute miles"
        elif loop_counter == 3:
            unit = "nautical miles"
        result = str(round((c * r),3))
        table.add_row([round(degrees(origin_lat),3), round(degrees(origin_lon),3), round(degrees(dest_lat),3), round(degrees(dest_lon),3), result, unit])
        loop_counter += 1
    print(table)

def main():
    print("Great Circle Distance Calculator")
    print("<==============================>")
    print("This tool accepts the lat and lon\nvalues of your origin and dest\nand then prints out the distance")
    print("between them in either nautical miles, statute miles, or kilometres.\n")

    origin_lat = get_origin_lat()
    origin_lon = get_origin_lon()
    dest_lat = get_dest_lat()
    dest_lon = get_dest_lon()
    haversine(origin_lon, origin_lat, dest_lon, dest_lat)

# Do the things!
main()