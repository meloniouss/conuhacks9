class Entity:
    brain = 0
    strength = 0
    aggression = 0
    faction = ""
    age = 0
    status = ""

    def __init__(self, faction, brain = 5, strength = 5, aggression = 5, age = 15, status = "alive"):
        self.faction = faction
        self.brain = brain
        self.strength = strength
        self.aggression = aggression
        self.age = age
        self.status = status

