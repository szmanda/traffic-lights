import time
from Database.database import Crossroad

TIME = 1 #seconds

# dict of combinations of roads that can be turned green at the same time
possibleCombinations = {
    1: ["in_road_n_0", "in_road_s_0", "out_road_n_0", "out_road_s_0"],
    2: ["in_sidewalk_e_0", "in_sidewalk_w_0"]
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
    
    print(bestCombination[0])
    # use chosen combination
    for name in  possibleCombinations[bestCombination[0]]:
        crossroad.greenLight(name)

def main():
    global crossroad
    crossroad = Crossroad("roadWithSidewalk")
    if len(crossroad.getRoadNames()) <= 0:
        print("initialise database!")
        exit()
    for _ in range(5):
        changeLights()
        time.sleep(TIME)

if __name__ == "__main__":
    main()