# Entity: Weather Observation

Based on the Smart Data Model for weather observation
[dataModel.Weather/WeatherObserved GitHub](https://github.com/smart-data-models/dataModel.Weather/tree/master/WeatherObserved)

Global description: A weather observation for the monitored area containing temperature, humidity and wind information

## List of properties

- 'dateObserved[date-time]': Date and time of observation in ISO 8601 UTC format
- 'id[string]': Unique id of the entity
- 'location[GeoJSON]': Physical location from where the observation was made described in GeoJSON format
    - 'type[string]': Type of GeoJSON geometry. Has to be Point
    - 'coordinates[array]': Array of coordinates for the location of the device. Has to be in the format '[latitude, longitude]'
- 'relativeHumidity[number]': Average humidity in the air for the area. Observed instantaneous relative humidity (water vapour in air)
- 'temperature[number]': Average temperature in the air for the area. Unit is degrees Celsius (°C)
- 'type[string]': NGSI Entity type. Is has to be WeatherObserved
- 'windSpeed[number]': Wind speed at the time of the observation. Unit is in meters per second (m/s)
- 'windDirection[number]': The azimuth that the wind is coming from at the time of observation. Unit is in degrees (°) ranging from 0° to 360°

Required properties

- 'dateObserved'
- 'id'
- 'location'
- 'relativeHumidity'
- 'temperature'
- 'type'
- 'windSpeed'
- 'windDirection'
