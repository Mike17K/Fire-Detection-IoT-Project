from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from typing import Tuple, List, Dict, Any

from context_broker import ContextBroker

app = FastAPI()
cb = ContextBroker("192.168.1.2")

class Tree(BaseModel):
    controlledProperty: List[str]
    dateObserved: datetime
    id: str
    location: Tuple[float, float]
    serialNumber: str
    type: str
    value: str

@app.post("/")
def get_data(data:Dict[Any, Any]):
    print(data)

import uvicorn, sys, os

if __name__ == "__main__":

    reload = "--reload" in sys.argv

    file = os.path.basename(sys.argv[0]).rstrip('.py')

    uvicorn.run(f"{file}:app", host="0.0.0.0", port=3001, reload=reload)
