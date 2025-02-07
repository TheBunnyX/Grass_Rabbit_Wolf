import random
import argparse
import matplotlib.pyplot as plt

#Command-line argument parsing
parser = argparse.ArgumentParser(description="Ecosystem simulation: Grass, Rabbits, and Wolves.")
parser.add_argument("--stage", type=int, default=0, help="Initial stage of the simulation")
parser.add_argument("--grow_rate", type=int, default=5, help="Grass growth rate per stage")
parser.add_argument("--count_grass", type=int, default=400, help="Initial amount of grass")
parser.add_argument("--count_rabbit", type=int, default=40, help="Initial number of rabbits")
parser.add_argument("--count_wolve", type=int, default=2, help="Initial number of wolves")
args = parser.parse_args()

#Assigning command-line arguments
stage = args.stage
grow_rate = args.grow_rate
count_grass = args.count_grass
count_rabbit = args.count_rabbit
count_wolve = args.count_wolve

#Grass class
class Grass:
    def __init__(self, count=count_grass, growth_rate=grow_rate):
        self.max_grass = count
        self.current_grass = count
        self.growth_rate = growth_rate

    def grow(self):
        self.current_grass = min(self.max_grass, self.current_grass + self.growth_rate)

#Rabbit class
class Rabbit:
    def __init__(self):
        self.current_food = 0
        self.max_food = 45
        self.metabolism = 3
        self.age = 0
        self.hunger_stages = 0

    def eat(self, grass):
        if grass.current_grass > 0:
            grass.current_grass -= 1
            self.current_food = min(self.max_food, self.current_food + 10)
            self.hunger_stages = 0  
            return True
        else:
            self.hunger_stages += 1
            return False

    def metabolize(self):
        self.current_food -= self.metabolism
        if self.current_food < 0:
            self.current_food = 0

    def reproduce(self):
        if self.age >= 10 and self.current_food >= 40 and random.random() < 0.5:
            return Rabbit()
        return None

    def is_alive(self):
        return self.hunger_stages < 3 and self.age < 25

#Wolf class
class Wolve:
    def __init__(self):
        self.current_food = 0
        self.max_food = 200
        self.metabolism = 2
        self.age = 0
        self.hunger_stages = 0

    def eat(self, rabbits):
        if rabbits and random.random() < 0.9:
            rabbit = random.choice(rabbits)
            rabbits.remove(rabbit)
            self.current_food = min(self.max_food, self.current_food + 10)
            self.hunger_stages = 0  
            return True
        else:
            self.hunger_stages += 1
            return False

    def metabolize(self):
        self.current_food -= self.metabolism
        if self.current_food < 0:
            self.current_food = 0

    def reproduce(self):
        if self.age >= 10 and self.current_food >= 120 and random.random() < 0.5:
            return Wolve()
        return None

    def is_alive(self):
        return self.hunger_stages < 2 and self.age < 50

#Initialize Grass, Rabbits, and Wolves
grass = Grass(count=count_grass, growth_rate=grow_rate)
rabbits = [Rabbit() for _ in range(count_rabbit)]
wolves = [Wolve() for _ in range(count_wolve)]

#Data for plotting
stages = []
grass_counts = []
rabbit_counts = []
wolf_counts = []
rabbit_eating = []
wolf_hunting = []
rabbit_births = []
wolf_births = []
rabbit_deaths = []
wolf_deaths = []

#Simulation loop
for stage in range(1, 101):  
    stages.append(stage)
    grass_counts.append(grass.current_grass)
    rabbit_counts.append(len(rabbits))
    wolf_counts.append(len(wolves))

    # Track statistics
    rabbits_ate = 0
    wolves_hunted = 0
    rabbit_born = 0
    wolf_born = 0
    rabbit_dead = 0
    wolf_dead = 0

    # Grass growth
    grass.grow()

    # Rabbits actions
    new_rabbits = []
    for rabbit in rabbits:
        if rabbit.eat(grass):
            rabbits_ate += 1
        rabbit.metabolize()
        rabbit.age += 1
        if rabbit.is_alive():
            baby = rabbit.reproduce()
            if baby:
                new_rabbits.append(baby)
                rabbit_born += 1
        else:
            rabbit_dead += 1

    rabbits = [rabbit for rabbit in rabbits if rabbit.is_alive()]
    rabbits.extend(new_rabbits)

    # Wolves actions
    new_wolves = []
    for wolf in wolves:
        if wolf.eat(rabbits):
            wolves_hunted += 1
        wolf.metabolize()
        wolf.age += 1
        if wolf.is_alive():
            baby = wolf.reproduce()
            if baby:
                new_wolves.append(baby)
                wolf_born += 1
        else:
            wolf_dead += 1

    wolves = [wolf for wolf in wolves if wolf.is_alive()]
    wolves.extend(new_wolves)

    # Store data
    rabbit_eating.append(rabbits_ate)
    wolf_hunting.append(wolves_hunted)
    rabbit_births.append(rabbit_born)
    wolf_births.append(wolf_born)
    rabbit_deaths.append(rabbit_dead)
    wolf_deaths.append(wolf_dead)

#Plot population dynamics
plt.figure(figsize=(12, 6))
plt.plot(stages, grass_counts, label='Grass', color='green')
plt.plot(stages, rabbit_counts, label='Rabbits', color='blue')
plt.plot(stages, wolf_counts, label='Wolves', color='red')
plt.title('Ecosystem Population Over Time')
plt.xlabel('Stage')
plt.ylabel('Population Count')
plt.legend()
plt.grid(True)
plt.savefig("population.png")
plt.show()

#Plot eating, reproduction, and death trends
plt.figure(figsize=(12, 6))
plt.plot(stages, rabbit_eating, label='Rabbits Eating', color='lightblue', linestyle='solid')
plt.plot(stages, wolf_hunting, label='Wolves Eating', color='darkred', linestyle='dashed')
plt.plot(stages, rabbit_births, label='Rabbit Births', color='blue', linestyle='solid')
plt.plot(stages, wolf_births, label='Wolf Births', color='red', linestyle='dashed')
plt.plot(stages, rabbit_deaths, label='Rabbit Deaths', color='purple', linestyle='solid')
plt.plot(stages, wolf_deaths, label='Wolf Deaths', color='black', linestyle='dashed')

plt.title('Ecosystem Eating, Reproduction, and Death Trends')
plt.xlabel('Stage')
plt.ylabel('Count per Stage')
plt.legend()
plt.grid(True)
plt.savefig("activity.png")
plt.show()
