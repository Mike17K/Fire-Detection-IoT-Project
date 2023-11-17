# Entity: Tree Sensor Observation

Based on the Smart Data Model for a generic device measurement
[dataModel.Device/DeviceMeasurement GitHub](https://github.com/smart-data-models/dataModel.Device/tree/master/DeviceMeasurement)

Global description: An observation of temperature, humidity and CO2 data from a tree sensor

## List of properties

- 'dateObserved[date-time]': Date and time of observation in ISO 8601 UTC format
- 'id[string]': Unique id of the entity
- 'location[GeoJSON]': Physical location of the observation described in GeoJSON format
    - 'type[string]': Type of GeoJSON geometry. Has to be Point
    - 'coordinates[array]': Array of coordinates for the location of the device. Has to be in the format '[latitude, longitude]'
- 'type[string]': NGSI Entity type. Is has to be DeviceMeasurement
- 'CO2[number]': CO2 levels measured by the device. Unit is parts per million (ppm)
- 'humidity[number]': Humidity measured by the device. Unit is percentage relative humidity (%RH)
- 'refDevice[string]': Id of the device that made the measurement
- 'temperature[number]': Temperature measured by the device. Unit is degrees Celsius (°C)

Required properties

- 'dateObserved'
- 'id'
- 'location'
- 'type'
- 'CO2'
- 'humidity'
- 'refDevice'
- 'temperature'
