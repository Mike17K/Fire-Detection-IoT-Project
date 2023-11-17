# Entity: Tree Sensor

Based on the Smart Data Model for a generic device
[dataModel.Device/Device GitHub](https://github.com/smart-data-models/dataModel.Device/tree/master/Device)

Global description: A sensor placed on a tree within a forest to gather temperature, humidity and CO2 data

## List of properties

- 'controlledProperty[array]': Data sensed by this sensor. It has to be the array '[CO2, humidity, temperature]'
- 'devEUI[string]': Unique device identifier
- 'id[string]': Unique id of the entity
- 'location[GeoJSON]': Physical location of the sensor described in GeoJSON format
    - 'type[string]': Type of GeoJSON geometry. Has to be Point
    - 'coordinates[array]': Array of coordinates for the location of the device. Has to be in the format '[latitude, longitude]'
- 'type[string]': NGSI Entity type. Is has to be Device

Required properties

- 'controlledProperty'
- 'devEUI'
- 'id'
- 'location'
- 'type'
