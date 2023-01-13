import os
from Database.database import Crossroad

if os.path.exists("Database/roadWithSidewalk.db"):
    os.remove("Database/roadWithSidewalk.db")
crossroad = Crossroad("roadWithSidewalk")
crossroad.newRoad(True, 'n', 0, False)
crossroad.newRoad(False, 'n', 0, False)
crossroad.newRoad(True, 's', 0, False)
crossroad.newRoad(False, 's', 0, False)
crossroad.newRoad(True, 'e', 0, True)
print(crossroad.getRoadNames())