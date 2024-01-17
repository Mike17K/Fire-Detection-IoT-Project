from fastapi import FastAPI, Request

from context_broker import ContextBroker

app = FastAPI()
cb = ContextBroker("192.168.1.2")

@app.get("/tree/{entity_id}")
@app.get("/wind/{entity_id}")
async def get_entity(entity_id):
    wind_sensor = cb.get_entity(entity_id)

    data = {
        "dateObserved": wind_sensor["dateObserved"],
        "id": entity_id,
        "location": wind_sensor["location"]["coordinates"],
    }

    tree_fields = wind_sensor["controlledProperty"]

    if wind_sensor["value"] is not None:
        tree_value = wind_sensor["value"].split("&")
    else:
        tree_value = [None for _ in range(len(tree_fields))]

    for i, field in enumerate(tree_fields):
        data[field] = tree_value[i]

    return data

@app.get("/temperature")
@app.get("/humidity")
@app.get("/co2")
async def get_tree_sensor_value(request: Request):
    tree_sensors = cb.get_tree_sensors()

    data = []
    requestedValueName = request.url.path.lstrip('/')

    for tree_sensor in tree_sensors:
        try:
            values = tree_sensor["value"].split("&")
            index = tree_sensor["controlledProperty"].index(requestedValueName)
            requestedValue = values[index]
        except:
            requestedValue = None

        temp = {
            "location": tree_sensor["location"]["coordinates"],
            requestedValueName: requestedValue
        }

        data.append(temp)

    return data

@app.get("/trees")
async def get_tree_sensor_values():
    tree_sensors = cb.get_tree_sensors()

    data = []

    for tree_sensor in tree_sensors:
        temp = {
            "location": tree_sensor["location"]["coordinates"],
            "co2": None,
            "humidity": None,
            "temperature": None,
        }
        try:
            values = tree_sensor["value"].split("&")

            for i, property in enumerate(tree_sensor["controlledProperty"]):
                temp[property] = values[i]
        except:
            pass

        data.append(temp)

    return data

import uvicorn, sys, os

if __name__ == "__main__":

    reload = "--reload" in sys.argv

    file = os.path.basename(sys.argv[0]).rstrip('.py')

    uvicorn.run(f"{file}:app", host="0.0.0.0", port=80, reload=reload)
