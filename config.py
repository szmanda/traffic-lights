import os
from Database.database import Crossroad

if os.path.exists("Database/roadWithSidewalk.db"):
    os.remove("Database/roadWithSidewalk.db")
crossroad = Crossroad("roadWithSidewalk")
crossroad.newRoad(True, False, 'n', 0)
crossroad.newRoad(False, False, 'n', 0)
crossroad.newRoad(True, False, 's', 0)
crossroad.newRoad(False, False, 's', 0)
crossroad.newRoad(True, True, 'e', 0)
crossroad.newRoad(True, True, 'w', 0)
print(crossroad.getRoadNames())
