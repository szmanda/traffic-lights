import sqlite3
import time
import json as js

class Crossroad:
    def __init__(self, name: str, path:str = "Database"):
        if path != "" and path[-1] != "/":
            path = path + "/" + name + ".db"
        else:
            path = path + name + ".db"
        self.__connection = sqlite3.connect(path)
        self.__cursor = self.__connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS roads(
            name varchar not null PRIMARY KEY,
            state varchar not null)"""
        self.__cursor.execute(query)
        query = """CREATE TABLE IF NOT EXISTS cars(
            time float not null,
            road varchar not null)"""
        self.__cursor.execute(query)
        self.__connection.commit()

    def newRoad(self, ingoing: bool, isSidewalk: bool, direction: str, num: int):
        if direction not in ('n', 'e', 'w', 's'):
            print("Wrong direction: ", direction, ", expected n, e, w or s")
            return
        name = "{0}_{1}_{2}_{3}".format("in" if ingoing else "out", "sidewalk" if isSidewalk else "road", direction, num)
        self.newRoadByName(name)
        return name

    def newRoadByName(self, name:str):
        query = "INSERT INTO roads values ('{0}', '{1}')".format(name, "red")
        self.__cursor.execute(query)
        self.__connection.commit()

    def newCar(self, roadName:str, timeOffset: float = 0, times:int = 1):
        t = time.time() - timeOffset
        query = f"""SELECT COUNT(*) FROM roads WHERE name='{roadName}'"""
        res = self.__cursor.execute(query)
        if(res.fetchone()[0] < 1):
            print(f"Road with name {roadName} does not exists!")
            return
        query = f"""INSERT INTO cars VALUES('{t}', '{roadName}')"""
        for _ in range(times):
            self.__cursor.execute(query)
            self.__connection.commit()

    def newCarByJson(self, jsonStr:str):
        json = js.loads(jsonStr)
        name = list(json.keys())[0]
        count = json[name]["count"]
        time_offset = json[name]["time_offset"]
        self.newCar(name, time_offset, count)

    def setNumberOfCars(self, jsonStr:str):
        json = js.loads(jsonStr)
        name = list(json.keys())[0]
        count = json[name]["count"]
        time_offset = json[name]["time_offset"]
        carsNum = self.getNumberOfCarsOnRoad(name)
        if count > carsNum:
            self.newCar(name, time_offset, count-carsNum)
        elif count < carsNum:
            self.passCar(name, count)
    
    def calculateImpatience(self, roadName: str):
        query = "SELECT time FROM cars WHERE road='{0}'".format(roadName)
        times = [x[0] for x in self.__cursor.execute(query).fetchall()]
        now = time.time()
        res = 0
        for x in times:
            res += (int(now - x) if x<now else 0)**2
        return res
    
    def greenLight(self, roadName: str):
        query = """UPDATE roads 
            SET state = 'green'
            WHERE name='{0}'""".format(roadName)
        self.__cursor.execute(query)
        self.__connection.commit()

    def redLight(self, roadName: str):
        query = """UPDATE roads 
            SET state = 'red'
            WHERE name={0}""".format(roadName)
        self.__cursor.execute(query)
        self.__connection.commit()
    
    def allRed(self):
        query = """UPDATE roads 
            SET state = 'red'"""
        self.__cursor.execute(query)
        self.__connection.commit()

    def getRoadsByImpatience(self):
        query = "SELECT name FROM roads WHERE name LIKE 'in%';"
        roads = [x[0] for x in self.__cursor.execute(query).fetchall()]
        impatience = []
        for x in roads:
            impatience.append(self.calculateImpatience(x))
        return [x for _, x in sorted(zip(impatience, roads), reverse=True)]

    def getRoadNames(self):
        query = "SELECT name FROM roads"
        roads = self.__cursor.execute(query)
        return [x[0] for x in roads.fetchall()]
    
    def getLight(self, roadName: str):
        query = f"SELECT state FROM roads WHERE name = '{roadName}'"
        return self.__cursor.execute(query).fetchone()[0]

    def getNumberOfCarsOnRoad(self, roadName: str):
        query = f"""SELECT COUNT(*) FROM cars WHERE road = '{roadName}' """
        return self.__cursor.execute(query).fetchone()[0]
    
    def passCarByJson(self, jsonStr:str):
        # json = {
        #     "in_road_n_0": {
        #         "count" : 1,
        #         "time_offset": 0
        #     }
        # }
        json = js.loads(jsonStr)
        name = list(json.keys())[0]
        count = json[name]["count"]
        self.passCar(name, count)
    
    def passCar(self, name:str, count:int):
        numberOfCars = self.getNumberOfCarsOnRoad(name)
        if count < 0:
            count += numberOfCars
        if numberOfCars <= 0 or count <= 0:
            return
        query = f"""DELETE FROM cars 
            WHERE rowid in 
            (SELECT rowid FROM cars 
            WHERE road = '{name}'
            ORDER BY time ASC
            LIMIT {count});"""
        self.__cursor.execute(query)
        self.__connection.commit()

