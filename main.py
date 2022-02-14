#collect pictures of around the earth
#sort them out 
from orbit import ISS
from skyfield.api import load

# Obtain the current time `t`
t = load.timescale().now()
# Compute where the ISS is at time `t`
position = ISS.at(t)
# Compute the coordinates of the Earth location directly beneath the ISS
location = position.subpoint()
print(location)

print(f'Latitude: {location.latitude}')
print(f'Longitude: {location.longitude}')
print(f'Elevation: {location.elevation.km}')

#
print(f'Lat: {location.latitude.degrees:.1f}, Long: {location.longitude.degrees:.1f}')

#this is when the camera is working
from time import sleep
from picamera import PiCamera
from pathlib import Path

base_folder = Path(__file__).parent.resolve()

camera = PiCamera()
camera.resolution = (1296,972)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(f"{base_folder}/image.jpg")

#CPU tempera†ure
from gpiozero import CPUTemperature

cpu = CPUTemperature()
print(cpu.temperature)
