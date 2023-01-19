# to install fastapi:
## pip install -r requirements.txt

# to run server
## in terminal type: uvicorn RestController:app --host=0.0.0.0 --reload
## server will run on port 8000, host 0.0.0.0 makes the api available in local network

from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

from Database.database import Crossroad


class RoadStateSetter(BaseModel):
    count:Optional[int]
    time_offset:Optional[int]

class StateAmendRequest(BaseModel):
    in_road_n_0:Optional[RoadStateSetter]
    in_road_s_0:Optional[RoadStateSetter]
    in_sidewalk_e_0:Optional[RoadStateSetter]
    in_sidewalk_w_0:Optional[RoadStateSetter]

databaseName = "roadWithSidewalk"
in_road_n_0 = "in_road_n_0"
in_road_s_0 = "in_road_s_0"
in_sidewalk_e_0 = "in_sidewalk_e_0"
in_sidewalk_w_0 = "in_sidewalk_w_0"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    print(newState)
    crossroad = Crossroad(databaseName)
    requestDict = newState.dict()
    roadDicts = ([{x[0]:x[1]} for x in list(requestDict.items())])
    for road in roadDicts:
        print("road: ", road)
        for roadName, attrib in road.items():
            if attrib != None:
                # print(roadName, attrib)
                crossroad.newCar(roadName, attrib["time_offset"], attrib["count"])
        

@app.put("/api/v1/set")
def setExpectant(newState:StateAmendRequest):
    crossroad = Crossroad(databaseName)
    # jakie zapyatnie do bazy?
    
