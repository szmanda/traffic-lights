import time
from Database.database import Crossroad

TIME = 5 #seconds

# dict of combinations of roads that can be turned green at the same time
possibleCombinations = {

}



def changeLights():
    # preparation
    roadsByImpatience = crossroad.getRoadsByImpatience()
    bestCombination = list(possibleCombinations.keys())
    crossroad.allRed()

    # get best combination
    for roadName in roadsByImpatience:
        withCurrRoad = bestCombination
        for key in bestCombination:
            if roadName not in possibleCombinations[key]:
                withCurrRoad.remove(key)
        if len(withCurrRoad) >= 1:
            bestCombination = withCurrRoad
        if len(bestCombination) <= 1:
            break

    # use chosen combination
    for name in  possibleCombinations[bestCombination[0]]:
        crossroad.greenLight(name)

def main():
    global crossroad
    crossroad = Crossroad("first")
    if len(crossroad.getRoadNames()) <= 0:
        print("initialise database!")
        exit()
    while True:
        changeLights()
        time.sleep(TIME)

if __name__ == "__main__":
    main()