import random

class Faction:
    name = ""
    area = 0
    membersCount = 0
    members = []
    brain = 0
    strength = 0
    aggression = 0
    status = ""

    DEATH_MULTIPLIER = 0.75

    def __init__(self, name, area = 0, membersCount = 0):
        self.name = name
        self.area = area
        self.membersCount = membersCount
        self.members = []
        self.status = "active"

    def addMember(self, ent):
        self.members.append(ent)
        self.membersCount += 1

    def calculateFactionStats(self):
        self.brain = 0
        self.strength = 0
        self.aggression = 0
        for ent in self.members:
            if ent.status == "alive":
                self.brain += ent.brain
                self.strength += ent.strength
                self.aggression += ent.aggression

    def incrementAge(self):
        for ent in self.members:
            if ent.status == "alive":
                ent.age += 1
                if ent.age >= 50:
                    deathChance = ent.age * self.DEATH_MULTIPLIER
                    deathRoll = random.randint(1, 100)
                    if deathRoll > deathChance:
                        ent.status = "dead"
                        self.membersCount -= 1