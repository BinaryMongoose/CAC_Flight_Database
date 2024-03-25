# CAC Flight Database
Database management for CAC's payloads.

If you want to add files to this database, they must be in this format.


## Data
The first column must be the time of the launch. 
Whether that's the duration of the flight, or actual time. 

The name of the sensor, underscore, and then the measurement. 
Everything lowercase. Only use the first 6 letter of the sensor.

Examples:
gps_time
bme288_temp
ltr90_uv

## Meta Data
This script automatically creates metadata, but it may not be accurate.

You can either use the supplied script to create metadata, or manually.