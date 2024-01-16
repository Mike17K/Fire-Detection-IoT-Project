from fastapi import FastAPI

from context_broker import ContextBroker

app = FastAPI()
cb = ContextBroker("192.168.1.2")

@app.get("/tree/{entity_id}")
@app.get("/wind/{entity_id}")
def get_entity(entity_id):
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
async def temperature():
    pass

@app.get("/humidity")
async def humidity():
    pass

@app.get("/co2")
async def co2():
    pass

@app.get("/wind")
async def wind():
    pass

import uvicorn, sys, os

if __name__ == "__main__":

    reload = "--reload" in sys.argv

    file = os.path.basename(sys.argv[0]).rstrip('.py')

    uvicorn.run(f"{file}:app", host="0.0.0.0", port=80, reload=reload)
