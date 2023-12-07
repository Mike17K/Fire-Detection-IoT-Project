# Entity: Wind Sensor

Based on the Smart Data Model for a generic device
[dataModel.Device/Device GitHub](https://github.com/smart-data-models/dataModel.Device/tree/master/Device)

Global description: A sensor placed on a tree within a forest to gather temperature, humidity and CO2 data

## List of properties

- 'controlledProperty[array]': Data sensed by this sensor. It has to be the array '[windDirection, windSpeed]'
- 'dateObserved[date-time]': Date and time of observation in ISO 8601 UTC format
- 'id[string]': Unique id of the entity
- 'location[GeoJSON]': Physical location of the sensor described in GeoJSON format
    - 'type[string]': Type of GeoJSON geometry. Has to be Point
    - 'coordinates[array]': Array of coordinates for the location of the device. Has to be in the format '[latitude, longitude]'
- 'serialNumber[string]': Unique device identifier. Is the same as the devEUI of the device. May change if device is replaced
- 'type[string]': NGSI Entity type. Is has to be Device
- 'value[String]': Current values of the sensor. The string consists of the values for measurements
    in the order in which they appear in the field "controlledProperty" separated by the character ";".
    Units are degrees (°) ranging from 0° to 360° for windDirection, meters per second (m/s) for windSpeed

Required properties

- 'controlledProperty'
- 'dateObserved'
- 'id'
- 'location'
- 'serialNumber'
- 'type'
- 'value'
