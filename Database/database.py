import sqlite3
import time


class Database:
    def __init__(self, patch:str, name: str):
        self.__connection = sqlite3.connect(patch + "/" + name + ".db")
        self.__cursor = self.__connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS roads(
            name varchar not null PRIMARY KEY,
            state varchar not null)"""
        self.__cursor.execute(query)
        query = """CREATE TABLE IF NOT EXISTS cars(
            time float not null,
            road varchar not null)"""
        self.__cursor.execute(query)

    def newRoad(self, ingoing: bool, direction: str, num: int):
        if direction not in ('n', 'e', 'w', 's'):
            print("Wrong direction: ", direction, ", expected n, e, w or s")
            return
        name = "{0}-road-{1}-{2}".format("in" if ingoing else "out", direction, num)
        query = "INSERT INTO roads values ('{0}', '{1}')".format(name, "red")
        self.__cursor.execute(query)
        self.__connection.commit()
        return name

    def newCar(self, time: float, roadName:str):
        query = """SELECT COUNT(*) FROM roads WHERE name='{0}'""".format(roadName)
        res = self.__cursor.execute(query)
        if(res.fetchone()[0] != 1):
            print("Road with name {0} does not exists!".format(roadName))
            return
        query = """INSERT INTO cars VALUES('{0}', '{1}')""".format(time, roadName)
        self.__cursor.execute(query)
        self.__connection.commit()

db = Database("Database", "test")
road = db.newRoad(True, 'n', 0)
db.newCar(time.time(), road)
db.newCar(time.time(), "road")
