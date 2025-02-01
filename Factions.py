import random
from Entities import Entity

class Faction:
    name = ""
    area = 0
    membersCount = 0
    members = []
    brain = 0
    strength = 0
    aggression = 0
    status = ""

    births = 0
    deaths = 0
    oldest = 0

    DEATH_MULTIPLIER = 0.75
    REPRODUCTION_MULTIPLIER = 0.25

    def __init__(self, name, area = 0, membersCount = 0):
        self.name = name
        self.area = area
        self.membersCount = membersCount
        self.members = []
        self.status = "active"

    def addMember(self):
        ent = Entity(faction = self.name)
        self.members.append(ent)
        self.membersCount += 1
        if self.status == "inactive":
            self.status = "active"

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
        self.births = 0
        self.deaths = 0
        self.oldest = 0
        for ent in self.members:
            if ent.status == "alive":
                ent.age += 1
                if ent.age >= 45:
                    deathChance = ent.age * self.DEATH_MULTIPLIER
                    deathRoll = random.randint(1, 100)
                    if deathChance > deathRoll:
                        ent.status = "dead"
                        self.membersCount -= 1
                        self.deaths += 1
                        if self.membersCount == 0:
                            self.status = "inactive"
            if ent.status == "alive":
                if ent.age >= 20:
                    reproductionRoll = random.randint(1, 100)
                    if reproductionRoll < self.REPRODUCTION_MULTIPLIER * 100:
                        self.births += 1
                if ent.age > self.oldest:
                    self.oldest = ent.age
        for x in range(self.births):
            self.addMember()

    def printFactionStats(self):
        print("Name: ", self.name, ", Status: ", self.status, ", Members: ", self.membersCount, ", New Births: ", self.births, ", New Deaths: ", self.deaths, ", Net Change: ", self.births - self.deaths, ", Oldest Member: ", self.oldest)