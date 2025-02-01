import threading
import time
from Factions import Faction

fact1 = Faction(name="Red")
fact2 = Faction(name="Blue")
fact3 = Faction(name="Green")

factions = [fact1, fact2, fact3]

def ageTimer(a):
    while True:
        time.sleep(a)
        for faction in factions:
            faction.incrementAge()
            faction.calculateFactionStats()

def ageMessage(a):
    print("{} minutes have passed. Increasing all entity ages by one...".format(a/60))

if __name__ == '__main__':
    ageThread = threading.Thread(target = ageTimer, args = (60, ageMessage(60)), daemon = True)

