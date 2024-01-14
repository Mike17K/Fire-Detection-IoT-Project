# Entity: Tree Sensor

Based on the Smart Data Model for a generic device
[dataModel.Device/Device GitHub](https://github.com/smart-data-models/dataModel.Device/tree/master/Device)

Global description: A sensor placed on a tree within a forest to gather temperature, humidity and CO2 data

## List of properties

- 'controlledProperty[array]': Data sensed by this sensor. It has to be the array '[CO2, humidity, temperature]'
- 'dateObserved[date-time]': Date and time of observation in ISO 8601 UTC format
- 'id[string]': Unique id of the entity
- 'location[GeoJSON]': Physical location of the sensor described in GeoJSON format
    - 'type[string]': Type of GeoJSON geometry. Has to be Point
    - 'coordinates[array]': Array of coordinates for the location of the device. Has to be in the format '[latitude, longitude]'
- 'serialNumber[string]': Unique device identifier. Is the same as the devEUI of the device. May change if device is replaced
- 'type[string]': NGSI Entity type. Is has to be Device
- 'value[String]': Current values of the sensors. The string consists of the values for the measurements
    in the order in which they appear in the field "controlledProperty" separated by the character "&".
    Units are parts per million (ppm) for CO2, relative humidity (%RH) for humidity, degrees Celsius (°C) for temperature

Required properties

- 'controlledProperty'
- 'dateObserved'
- 'id'
- 'location'
- 'serialNumber'
- 'type'
- 'value'
