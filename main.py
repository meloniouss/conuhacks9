import threading
import time
from Factions import Faction

fact1 = Faction(name="Red")
fact2 = Faction(name="Blue")
fact3 = Faction(name="Green")

factions = [fact1, fact2, fact3]

for x in range(10):
    for faction in factions:
        faction.addMember()


def ageTimer(a, message):
    while True:
        time.sleep(a)
        message(a)
        for faction in factions:
            faction.incrementAge()
            faction.calculateFactionStats()
            faction.printFactionStats()

def ageMessage(a):
    print("\n\n{} minutes have passed. Increasing all entity ages by one...".format(a/60))

if __name__ == '__main__':
    ageThread = threading.Thread(target = ageTimer, args = (1, ageMessage), daemon = True)
    ageThread.start()

    while True:
        print("Main program is running...")
        time.sleep(60)  # Simulating other tasks

