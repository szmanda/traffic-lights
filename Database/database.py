import sqlite3
import time

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

    def newRoad(self, ingoing: bool, direction: str, num: int, isSidewalk: bool):
        if direction not in ('n', 'e', 'w', 's'):
            print("Wrong direction: ", direction, ", expected n, e, w or s")
            return
        name = "{0}-{1}-{2}-{3}".format("in" if ingoing else "out", "sidewalk" if isSidewalk else "road", direction, num)
        self.newRoadByName(name)
        return name

    def newRoadByName(self, name:str):
        query = "INSERT INTO roads values ('{0}', '{1}')".format(name, "red")
        self.__cursor.execute(query)
        self.__connection.commit()

    def newCar(self, time: float, roadName:str):
        query = """SELECT COUNT(*) FROM roads WHERE name='{0}'""".format(roadName)
        res = self.__cursor.execute(query)
        if(res.fetchone()[0] < 1):
            print("Road with name {0} does not exists!".format(roadName))
            return
        query = """INSERT INTO cars VALUES('{0}', '{1}')""".format(time, roadName)
        self.__cursor.execute(query)
        self.__connection.commit()
    
    def calculateImpatience(self, roadName: str):
        query = "SELECT time FROM cars WHERE road='{0}'".format(roadName)
        times = [x[0] for x in self.__cursor.execute(query).fetchall()]
        now = time.time()
        res = 0
        for x in times:
            res += int(now - x)**2
        return res
    
    def greenLight(self, roadName: str):
        query = """UPDATE roads 
            SET state = 'green'
            WHERE name='{0}'""".format(roadName)
        self.__cursor.execute(query)
        self.__connection.commit()
        query = "DELETE FROM cars WHERE road='{0}'".format(roadName)
        self.__cursor.execute(query)
        self.__connection.commit()
        # TODO pass certain number of cars

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
        query = "SELECT name FROM roads"
        roads = [x[0] for x in self.__cursor.execute(query).fetchall()]
        keys = []
        for x in roads:
            keys.append(self.calculateImpatience(x))
        return [x for _, x in sorted(zip(keys, roads))]

    def getRoadNames(self):
        query = "SELECT name FROM roads"
        roads = self.__cursor.execute(query)
        return [x[0] for x in roads.fetchall()]
    
    def getLight(self, roadName: str):
        query = f"SELECT state FROM roads WHERE name = '{roadName}'"
        return self.__cursor.execute(query).fetchone()[0]

# db = Crossroad("test", "Database")
# roadNames = db.getRoadNames()
# if len(roadNames)>0:
#     road = roadNames[0]
# else:
#     road = db.newRoad(True, 'n', 0, False)
# db.newCar(time.time(), road)
# time.sleep(1)
# db.newCar(time.time(), road)
# time.sleep(2)
# db.newCar(time.time(), road)
# print(db.calculate(road))