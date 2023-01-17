# to install fastapi:
## pip install -r requirements.txt

# to run server
## in terminal type: uvicorn RestController:app --reload
## server will run on port 8000

from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

from Database.database import Crossroad


class RoadStateSetter(BaseModel):
    count:int
    time_offset:int

class StateAmendRequest(BaseModel):
    in_road_n_0:RoadStateSetter
    in_road_s_0:RoadStateSetter
    in_sidewalk_e_0:RoadStateSetter
    in_sidewalk_w_0:RoadStateSetter

databaseName = "roadWithSidewalk"
in_road_n_0 = "in_road_n_0"
in_road_s_0 = "in_road_s_0"
in_sidewalk_e_0 = "in_sidewalk_e_0"
in_sidewalk_w_0 = "in_sidewalk_w_0"

app = FastAPI()

@app.get("/api/v1/state")
def getState():
    crossroad = Crossroad(databaseName)

    inRoadNorth0Light = crossroad.getLight(in_road_n_0)
    inRoadSouthh0Light = crossroad.getLight(in_road_s_0)

    inSidewalkEast0Light = crossroad.getLight(in_sidewalk_e_0)
    inSidewalkWest0Light = crossroad.getLight(in_sidewalk_w_0)

    inRoadNorth0Count = crossroad.getNumberOfCarsOnRoad(in_road_n_0)
    inRoadSouthh0Count = crossroad.getNumberOfCarsOnRoad(in_road_s_0)
    inSidewalkEast0Count = crossroad.getNumberOfCarsOnRoad(in_sidewalk_e_0)
    inSidewalkWest0Count = crossroad.getNumberOfCarsOnRoad(in_sidewalk_w_0)

    return {
            in_road_n_0: {"light":inRoadNorth0Light, "waiting_count": inRoadNorth0Count},
            in_road_s_0: {"light":inRoadSouthh0Light, "waiting_count": inRoadSouthh0Count},
            in_sidewalk_e_0: {"light":inSidewalkEast0Light, "waiting_count": inSidewalkEast0Count},
            in_sidewalk_w_0: {"light":inSidewalkWest0Light, "waiting_count": inSidewalkWest0Count}
    }

@app.delete("/api/v1/remove")
def removeExpectant(newState:StateAmendRequest):
    crossroad = Crossroad(databaseName)

    requestDict = newState.dict()
    roadDicts = ([{x[0]:x[1]} for x in list(requestDict.items())])
    for road in roadDicts:
        crossroad.passCar(road)
    
@app.post("/api/v1/add")
def addExpectant(newState:StateAmendRequest):
    crossroad = Crossroad(databaseName)

    requestDict = newState.dict()
    roadDicts = ([{x[0]:x[1]} for x in list(requestDict.items())])
    for road in roadDicts:
        for roadName, attrib in road.items():
             crossroad.newCar(roadName, attrib["time_offset"], attrib["count"])
        

@app.put("/api/v1/set")
def setExpectant(newState:StateAmendRequest):
    crossroad = Crossroad(databaseName)
    # jakie zapyatnie do bazy?
    
