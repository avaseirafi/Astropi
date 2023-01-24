import csv
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

from logzero import logfile, logger
from orbit import ISS
from picamera import PiCamera

def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    location = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    camera.capture(image)


base_folder = Path(__file__).parent.resolve()

# Set a logfile name
logfile(base_folder/"flight.log")

# Set up camera
cam = PiCamera()
cam.resolution = (1296, 972)

# Initialise the CSV file
data_file = base_folder/"data.csv"
create_csv_file(data_file)

# Initialise the photo counter
counter = 1
# Record the start and current time
start_time = datetime.now()
now_time = datetime.now()

"""
TODO: FILTER, FREQUENCY, LOCATION
Filter out certain unnecessary images 
(blue: ocean, lakes, bodies of water, greenery: 
fields, grass, vegetation, black: unclear bad photos, nighttime, white: clouds)
Frequency of photos, how many photos per how many seconds, 
Gps location of where desertification is going to occur depending on the 
location of iss in its orbit
Taking more photos in areas known for desertification
 """

# Run a loop for just under 3 hours
while (now_time < start_time + timedelta(minutes=179)):
    try:
        # Get coordinates of location on Earth under the ISS
        location = ISS.coordinates()
        # Save the data to the file
        data = (
            counter,
            datetime.now(),
            location.latitude.degrees,
            location.longitude.degrees,
        )
        add_csv_data(data_file, data)
        # Capture image
        image_file = f"{base_folder}/photo_{counter:04d}.jpg"
        capture(cam, image_file)
        # Log event
        logger.info(f"iteration {counter}")
        counter += 1
        sleep(30)
        # Update the current time
        now_time = datetime.now()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')
