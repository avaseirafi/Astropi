#!/usr/bin/env python3
from orbit import ISS
from skyfield.api import load


def print_iss_location():
    # Obtain the current time `t`
    t = load.timescale().now()
    # Compute where the ISS is at time `t`
    position = ISS.at(t)
    # Compute the coordinates of the Earth location directly beneath the ISS
    location = position.subpoint()
    print(location)
    print(f"Latitude: {location.latitude}")
    print(f"Longitude: {location.longitude}")
    print(f"Elevation: {location.elevation.km}")
    print(f"Lat: {location.latitude.degrees:.2f}, Long: {location.longitude.degrees:.2f}")

def main():
    print_iss_location()

# run main with when not imported
if __name__ == "__main__":
    main()
