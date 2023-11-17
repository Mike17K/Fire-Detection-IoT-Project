# Entity: Fire Forest Status

Based on the Smart Data Model for Fire Forest Status
[dataModel.Forestry/FireForsetStatus GitHub](https://github.com/smart-data-models/dataModel.Forestry/tree/master/FireForsetStatus)

Global description: Entity describing the possible presence of a fire in a forest

## List of properties

- 'dateCreated[date-time]': Date and time that the entity was created in ISO 8601 UTC format
- 'fireDetected[boolean]': Presence of a fire detected in the area
- 'fireDetectedConfidence[number]': Confidence in the fire detection as a percentage from 0 to 1
- 'fireRiskIndex[number]': Risk of fire index as a percentage from 0 to 1
- 'id[string]': Unique id of the entity
- 'location[GeoJSON]': Physical location of the area served in GeoJSON format
    - 'type[string]': Type of GeoJSON geometry
    - 'coordinates[array]': Array of coordinates
- 'type[string]': NGSI Entity type. Is has to be FireForestStatus

Required properties

- 'dateCreated'
- 'id'
- 'location'
- 'type'
