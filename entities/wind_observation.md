# Entity: Wind Observation

Based on the Smart Data Model for weather observation
[dataModel.Weather/WeatherObserved GitHub](https://github.com/smart-data-models/dataModel.Weather/tree/master/WeatherObserved)

Global description: A weather observation containing only wind data

## List of properties

- 'dateObserved[date-time]': Date and time of observation in ISO 8601 UTC format
- 'id[string]': Unique id of the entity
- 'location[GeoJSON]': Physical location from where the observation was made described in GeoJSON format
    - 'type[string]': Type of GeoJSON geometry. Has to be Point
    - 'coordinates[array]': Array of coordinates for the location of the device. Has to be in the format '[latitude, longitude]'
- 'type[string]': NGSI Entity type. Is has to be WeatherObserved
- 'windSpeed[number]': Wind speed at the time of the observation. Unit is in meters per second (m/s)
- 'windDirection[number]': The azimuth that the wind is coming from at the time of observation. Unit is in degrees (°) ranging from 0° to 360°

Required properties

- 'dateObserved'
- 'id'
- 'location'
- 'type'
- 'windSpeed'
- 'windDirection'
