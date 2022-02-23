#!/usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

from orbit import ISS
from picamera import PiCamera
from skyfield.api import load

# set base folder for path resolution
base_folder = Path(__file__).parent.resolve()

#setting up the picamera
camera = PiCamera()
camera.resolution = (1296, 972)
camera.start_preview()
# Camera warm-up time
sleep(2)


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
    print(f"Lat: {location.latitude.degrees:.1f}, Long: {location.longitude.degrees:.1f}")

def capture_picture(name):
    # Take a single picture
    camera.capture(f"{base_folder}/{name}_image.jpg")


def convert_pictures(files):
    # capturing the pictures and converting them to files we can open
    print("converting images will be handled in the Cloud not above on the ISS")


def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f"{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10"
    return sign < 0, exif_angle


def capture_gpstaggedphoto(name):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    point = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags["GPS.GPSLatitude"] = exif_latitude
    camera.exif_tags["GPS.GPSLatitudeRef"] = "S" if south else "N"
    camera.exif_tags["GPS.GPSLongitude"] = exif_longitude
    camera.exif_tags["GPS.GPSLongitudeRef"] = "W" if west else "E"

    # Capture the image
    camera.capture(image)

    base_folder = Path(__file__).parent.resolve()
    capture(camera, f"{base_folder}/{name}gps1.jpg")


def capture_image_every(seconds = 30, for_hours=3):
    for i in range(for_hours*60*(60/seconds)):
        camera.capture(f'{base_folder}/image_{i:03d}.jpg')  # Take a picture every minute for 3 hours
        print(f"Captured {base_folder}/image_{i:03d}.jpg")
        sleep(seconds)


# Using os.system to Run a Command
# Python allows us to immediately execute a shell command that's stored in a string using the os.system() function.
# for this to work the ffmpeg command must be wrapped with os.system()
# def print_create (timelapse):
# creates a timelapse movie from the pictures taken in the code before
# ffmpeg -framerate 10 -i %*.jpg -c:v libx264 -crf 17 -pix_fmt yuv420p timelapse.mp4

# Again the any commands that are to be run on using the terminal bust be wrapped with os.system
# def print_resolution (photos):
# fixes the resolution of the photos
# sudo raspi-config


def print_timespan(three_hours):
    # running our experiment for 3 hours

    # Create a `datetime` variable to store the start time
    start_time = datetime.now()
    # Create a `datetime` variable to store the current time
    # (these will be almost the same at the start)
    now_time = datetime.now()
    # Run a loop for 2 minutes
    while now_time < start_time + timedelta(minutes=2):
        print("Doing stuff")
        sleep(1)
        # Update the current time
        now_time = datetime.now()

#Defining Python’s main function is not mandatory, 
#but it is a good practice to do so for better readability 
#of you program and more importantly allows for better reuse.

def main():
    capture_image_every(10, 0.16)

# run main with when not imported
if __name__ == "__main__":
    main()