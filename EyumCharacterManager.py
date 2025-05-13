import random
import time
import os
import json

# This program manages and creates characters for the world of Eyum.
# It focuses on combat stats (not roleplay stats).

# TODO
# 1. Add classes to the character creation section as well as their subclasses and level 1 features
# 2. Add functionality for the therinthropes and halflings (they need a lot more manual effort than a normal race and it is currently impossible)
# 3. Add level ups to the character manager wich follow the handbook and can save
# 4. Add a combat simulation section where it allows you to choose two saved characters and simulate a fight to see who would win (runs mostly randomly)
# 5. Make everything look much nicer with colors and good spacing and timing, all that good fluff

# === Race Definitions ===
# Lists of racial attributes and bonuses for each race (indexed by raceId).
raceId = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
raceNames = ["arborelin", "aurian", "avian", "dwarf", "elf", "elnar", "ferramite", "giant", "grivlit",
             "halfling", "human", "iceborn", "ignites", "lumari", "mireglopians", "naga", "nyctaris",
             "slamandrains", "spritelings", "stingerfolk", "stonekin", "sylphmare", "syrith", "therianthropes", "zephar"]
# Size categories: 0=Tiny, 1=Small, 2=Medium, 3=Large, 4=Huge
raceSize = [3, 2, 2, 2, 1, 2, 2, 4, 1, -1, 2, 2, 2, 2, 2, 3, 1, 1, 0, 3, 3, 2, 2, 2, 2]
raceSpeed = [25, 30, 25, 25, 30, 30, 30, 35, 30, -1, 25, 25, 30, 30, 25, 35, 30, 30, 20, 30, 30, 35, 30, 25, 25]
raceFlyingSpeed = [0, 0, 60, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 35, 0, 0]
raceSwimSpeed = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 40, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Racial affinity adjustments (positive or negative predispositions to certain elements/skills)
raceFireAffinity = [-10, 0, 0, 0, -10, -10, 0, -5, -5, -1, -5, -10, 5, 0, -10, 0, -10, 0, -5, 0, 0, -10, -10, -5, 0]
raceEarthAffinity = [-5, 0, -10, 0, 0, -5, 0, 0, -10, -1, -5, -5, -5, 0, -10, 0, -10, 0, -5, 0, 0, -10, -10, -5, 0]
raceWaterAffinity = [0, 0, -5, -5, 0, 0, -10, -10, -10, -1, -5, 0, -10, 0, 0, 0, -10, -10, -10, 0, 0, -10, 0, -5, -10]
raceAirAffinity = [0, 0, 0, -5, 0, 0, -10, -10, 0, -1, -5, 0, 0, 0, -10, 0, -10, -10, -10, -10, 0, -10, 0, -5, -10]
raceCreateAffinity = [0, 0, -5, 0, -5, 0, -5, 0, -10, -1, 0, 0, -10, 0, 0, -10, -10, -5, 0, -10, 0, -10, -5, -5, 0]
raceCraftAffinity = [-10, 0, -10, 0, -5, -10, -5, -5, 0, -1, 0, -5, -10, -10, 0, -10, -10, -5, 0, -10, -10, -10, -5, -5, 0]
raceUtilityAffinity = [-10, 0, -5, 0, -5, -10, 0, -5, 0, -1, 0, 0, -10, -10, 0, -10, -10, -5, 0, -10, -10, -10, 0, -5, 0]
racePhysicalAffinity = [0, 0, 0, 0, -5, 0, 0, 0, -5, -1, 0, 0, -10, -10, 0, -10, -10, 0, 0, 0, 0, -10, -10, -5, -5]
raceGenericAffinity = [0, 0, -5, -5, 0, 0, 0, -10, -5, -1, -5, 0, 0, -5, 0, -5, -5, -5, -5, -5, -5, -10, -5, -5, -5]

# Racial stat bonuses to base attributes
raceStrBonus = [5, 0, 0, 0, 0, 0, 3, 5, -3, -1, 1, 0, 0, 0, 5, 2, 0, 0, -3, 3, 4, 0, 0, 0, 2]
raceConBonus = [4, 0, 0, 1, -1, 0, 3, 3, -3, -1, 1, 0, -1, 0, 15, 3, 0, 10, -3, 2, 10, 0, 0, 0, 1]
raceDexBonus = [0, 0, 4, 0, 3, 0, 0, -4, 4, -1, 1, 0, 2, 0, 0, 1, 0, 2, 3, 1, 0, 0, 0, 0, 0]
raceIntBonus = [0, 4, -2, 0, 0, 0, 0, -4, 1, -1, 1, 3, 0, 0, -10, -1, 0, -4, -5, -1, -5, 0, 0, 0, -2]
raceWisBonus = [0, 5, 0, 0, 2, 0, 0, -4, 0, -1, 1, 4, 3, 3, -10, -1, 0, -4, -3, -1, -4, 0, 2, 0, 0]
raceCharBonus = [0, 0, 0, 0, 5, 0, 0, -2, 0, -1, 1, 0, 0, 0, 0, -3, 0, -2, 2, -3, -5, 6, 5, 0, 0]

# Racial resistances (0 = none, 1 = half damage, 2 = immunity, -1 = weakness)
raceFireResist = [0, 0, 0, 0, 0, 0, 1, 1, 0, -1, 0, 1, 2, 0, -1, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0]
raceColdResist = [0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 2, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0]
racePoisonResit = [0, 0, 0, 1, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0]
raceAirResit = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
raceWaterResist = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
raceSlashingResist = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]
raceBludgeRestist = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -1, 2, 0, 0]
racePeirceResist = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]

# === Class Definitions ===
# (Work in progress: classes, subclasses, and related stats)
classNames = ["Fighter",]
subclass1 = ["Blade Master"]
subclass2 = []
subclass3 = []
subclass4 = []
# Class type: 1 = Physical, 2 = Magical, 3 = Both
classType = [1,]
classVitalityDice = ["2d12"]
classHitDice = ["2d8"]
classManaDice = ["1d4"]
classProfficiency = [2,]

classVitalityBonus = [10,]
classHealthBonus = [5,]
classManaBonus = [0,]

# TODO: Define class weapons and armor (to be implemented)
classWeaponsSwords = []
classWeapons = []
classArmor = []

# === Global Character Variables ===
# These store the current character's info and stats.
# Character identity
characterName = ""
characterRace = ""

# Base stats (attributes)
characterStr = 0
characterCon = 0
characterDex = 0
characterInt = 0
characterWis = 0
characterChar = 0

# Affinity stats
characterAffinityFire = 0
characterAffinityEarth = 0
characterAffinityWater = 0
characterAffinityAir = 0
characterAffinityCraft = 0
characterAffinityCreation = 0
characterAffinityPhysical = 0
characterAffinityUtility = 0
characterAffinityGeneric = 0

# Combat stats and actions
characterActions = 1
characterBonusActions = 1
characterReactions = 1
characterInitiative = 0
characterAc = 0
characterSpeed = 0

# Other Variables
randomSelected = False
first_names = [
    "Zarnak", "Velthra", "Korrin", "Xaviel", "Thindrel", "Braxin", "Yureth", "Omariq", "Selqen", "Hadrik",
    "Jasryl", "Vorne", "Drelith", "Qimara", "Lazrin", "Norys", "Thazul", "Eryndor", "Mavrix", "Ulvien",
    "Zarlek", "Orthis", "Kirel", "Yenvar", "Marnix", "Zevran", "Valkor", "Tirian", "Elixor", "Durien",
    "Xelra", "Inzali", "Varnak", "Revik", "Syrix", "Molgar", "Nivelle", "Osvarn", "Vessari", "Torvek",
    "Zarmina", "Kelzor", "Yrissa", "Tholen", "Iskral", "Narvyn", "Valeth", "Qorlan", "Tazmere", "Drovik",
    "Relgar", "Yanthir", "Selvra", "Harkel", "Zurnia", "Vorren", "Tivrak", "Ilyzan", "Braskin", "Xirzel",
    "Jorvek", "Mireth", "Kalzor", "Vorlia", "Sarnok", "Yalven", "Threxil", "Vandrin", "Irrik", "Droxal",
    "Qelrin", "Nyzari", "Karven", "Xulren", "Orrith", "Velmin", "Zolkar", "Lirien", "Vaskar", "Thalvek",
    "Zirel", "Korvex", "Mordai", "Zavien", "Qintra", "Rhelan", "Eryss", "Volrek", "Tarnyx", "Jasker",
    "Zenthos", "Urazel", "Narlis", "Krezal", "Yuvin", "Sarlix", "Vorlin", "Tazrak", "Ryxen", "Drelzar"
]

last_names = [
    "Grathmoor", "Veldrake", "Zarnith", "Krellthorn", "Orrivar", "Malgrin", "Dravosh", "Elvaron", "Fyrthain", "Korathir",
    "Tharvok", "Yandros", "Morrix", "Skeldorn", "Verathen", "Droxigar", "Zhaldrin", "Qelvorn", "Rynthor", "Nazhik",
    "Tarnoss", "Xeradon", "Vrimloch", "Kelgroth", "Zhurvar", "Lazthar", "Vandross", "Molgarin", "Threxlor", "Jarneth",
    "Ulgryn", "Skavren", "Durvak", "Ombrith", "Zarkhul", "Renvok", "Yarstrix", "Varkell", "Drasthorn", "Egrador",
    "Silzaren", "Qarthor", "Kelbrin", "Narvok", "Vondrek", "Tharziel", "Izmarn", "Zellvok", "Korbrith", "Zernash",
    "Delmorr", "Ulgorin", "Braxthor", "Mordros", "Zenthari", "Yarlven", "Gravrix", "Thundrak", "Zarvalin", "Kurnash",
    "Vellmor", "Qarnith", "Velgrin", "Dralven", "Krezmor", "Orlavik", "Zarneth", "Xanvur", "Norrivan", "Yelbrik",
    "Zalgrin", "Vyrnock", "Drelvash", "Skarnix", "Quarnel", "Thokmir", "Ulzarith", "Kerothan", "Marqwin", "Zorlinth",
    "Velqros", "Zundros", "Kervash", "Dranquin", "Myrrvik", "Oznaril", "Grelthor", "Trunvak", "Sylvarik", "Yaldrin",
    "Malreth", "Kharvos", "Tylroth", "Vornask", "Zherikon", "Qurimoth", "Keldrix", "Nyvrin", "Zavrok", "Olverin"
]

# === Program Start and Main Menu ===
# Entry point: welcomes user and presents main menu options
def firstTime():
    print("Welcome to Eyum Character Manager!")
    main()

# Main menu loop: choose to create a new character or manage an existing one
def main():
    print("What would you like to do? [0 = Make a character  |  1 = Manage a saved character]")
    choice = input()
    time.sleep(0.5)
    if choice == "0":
        createCharacter()
    elif choice == "1":
        manageCharacter()
    else:
        print("That is not a valid input")
    main()

# === Character Save/Load Functions ===
# Save current character to a file, or load an existing character from a file
def saveCharacter():
    global characterName
    # Ensure save directory exists
    save_dir = "SavedCharacters"
    os.makedirs(save_dir, exist_ok=True)
    # Prepare data dictionary
    save_data = {
        "name": characterName,
        "race": characterRace,
        "str": characterStr,
        "con": characterCon,
        "dex": characterDex,
        "int": characterInt,
        "wis": characterWis,
        "char": characterChar,
        "affinity_fire": characterAffinityFire,
        "affinity_earth": characterAffinityEarth,
        "affinity_water": characterAffinityWater,
        "affinity_air": characterAffinityAir,
        "affinity_craft": characterAffinityCraft,
        "affinity_creation": characterAffinityCreation,
        "affinity_physical": characterAffinityPhysical,
        "affinity_utility": characterAffinityUtility,
        "affinity_generic": characterAffinityGeneric,
        "actions": characterActions,
        "bonus_actions": characterBonusActions,
        "reactions": characterReactions,
        "initiative": characterInitiative,
        "ac": characterAc,
        "speed": characterSpeed
    }
    filepath = os.path.join(save_dir, f"{characterName}.json")
    with open(filepath, "w") as f:
        json.dump(save_data, f, indent=4)
    print(f"\nCharacter '{characterName}' saved to '{filepath}'.")

def loadCharacter():
    global characterName, characterRace, characterStr, characterCon, characterDex, characterInt, characterWis, characterChar
    global characterAffinityFire, characterAffinityEarth, characterAffinityWater, characterAffinityAir
    global characterAffinityCraft, characterAffinityCreation, characterAffinityPhysical
    global characterAffinityUtility, characterAffinityGeneric
    global characterActions, characterBonusActions, characterReactions
    global characterInitiative, characterAc, characterSpeed
    filename = input("Enter the name of the character to load: ")
    filepath = os.path.join("SavedCharacters", f"{filename}.json")
    if not os.path.exists(filepath):
        print("Character file not found.")
        return
    with open(filepath, "r") as f:
        data = json.load(f)
    # Load data into global variables
    characterName = data.get("name", "")
    characterRace = data.get("race", "")
    characterStr = data.get("str", 0)
    characterCon = data.get("con", 0)
    characterDex = data.get("dex", 0)
    characterInt = data.get("int", 0)
    characterWis = data.get("wis", 0)
    characterChar = data.get("char", 0)
    characterAffinityFire = data.get("affinity_fire", 0)
    characterAffinityEarth = data.get("affinity_earth", 0)
    characterAffinityWater = data.get("affinity_water", 0)
    characterAffinityAir = data.get("affinity_air", 0)
    characterAffinityCraft = data.get("affinity_craft", 0)
    characterAffinityCreation = data.get("affinity_creation", 0)
    characterAffinityPhysical = data.get("affinity_physical", 0)
    characterAffinityUtility = data.get("affinity_utility", 0)
    characterAffinityGeneric = data.get("affinity_generic", 0)
    characterActions = data.get("actions", 1)
    characterBonusActions = data.get("bonus_actions", 1)
    characterReactions = data.get("reactions", 1)
    characterInitiative = data.get("initiative", 0)
    characterAc = data.get("ac", 0)
    characterSpeed = data.get("speed", 0)
    print(f"\nCharacter '{characterName}' loaded successfully.")

def listSavedCharacters():
    save_dir = "SavedCharacters"
    if not os.path.exists(save_dir):
        print("No saved characters found.")
        return

    files = [f for f in os.listdir(save_dir) if f.endswith(".json")]
    if not files:
        print("No saved characters found.")
        return

    print("\nSaved Characters:")
    for f in files:
        print(" -", f[:-5])  # Strip .json extension

# === Race Information Display ===
# Print the affinities, stat bonuses, and resistances for a given race index
def racialStatsBonuses(raceIndex, choice):
    # Compile affinities into lines for display
    affinities = [
        ("Fire", raceFireAffinity[raceIndex]),
        ("Craft", raceCraftAffinity[raceIndex]),
        ("Earth", raceEarthAffinity[raceIndex]),
        ("Physical", racePhysicalAffinity[raceIndex]),
        ("Water", raceWaterAffinity[raceIndex]),
        ("Utility", raceUtilityAffinity[raceIndex]),
        ("Air", raceAirAffinity[raceIndex]),
        ("Creation", raceCreateAffinity[raceIndex]),
        ("Generic", raceGenericAffinity[raceIndex])
    ]
    affinity_lines = []
    line = ""
    for i, (name, val) in enumerate(affinities):
        if val != 0:
            line += f"{name}: {val}  "
        if (i + 1) % 2 == 0:
            affinity_lines.append(line.strip())
            line = ""
    if line:
        affinity_lines.append(line.strip())
    print(f"{choice} has the following AFFINITY bonuses:")
    for l in affinity_lines:
        print(l)
    # Compile stat bonuses line
    stats = [
        ("Str", raceStrBonus[raceIndex]),
        ("Wis", raceWisBonus[raceIndex]),
        ("Con", raceConBonus[raceIndex]),
        ("Int", raceIntBonus[raceIndex]),
        ("Dex", raceDexBonus[raceIndex]),
        ("Char", raceCharBonus[raceIndex])
    ]
    stat_line = " ".join(f"{name}: {val}" for name, val in stats if val != 0)
    if stat_line:
        print(f"{choice} has the following STAT bonuses:")
        print(stat_line)
    # Compile resistances
    resistances = [
        ("Fire", raceFireResist[raceIndex]),
        ("Cold", raceColdResist[raceIndex]),
        ("Poison", racePoisonResit[raceIndex]),
        ("Air", raceAirResit[raceIndex]),
        ("Water", raceWaterResist[raceIndex]),
        ("Slashing", raceSlashingResist[raceIndex]),
        ("Bludgeoning", raceBludgeRestist[raceIndex]),
        ("Piercing", racePeirceResist[raceIndex])
    ]
    resistance_lines = []
    for name, val in resistances:
        if val == 1:
            resistance_lines.append(f"Resistant to {name}")
        elif val == 2:
            resistance_lines.append(f"Immune to {name}")
        elif val == -1:
            resistance_lines.append(f"Weak to {name}")
    if resistance_lines:
        print(f"{choice} has the following RESISTANCE traits:")
        for line in resistance_lines:
            print(line)

# === Character Creation Functions ===
# Race selection, stat allocation, affinity assignment, and character finalization
def buildCharacter():
    global characterStr, characterCon, characterDex, characterInt, characterWis, characterChar
    global characterAffinityFire, characterAffinityEarth, characterAffinityWater, characterAffinityAir
    global characterAffinityCraft, characterAffinityCreation, characterAffinityPhysical
    global characterAffinityUtility, characterAffinityGeneric
    raceIndex = raceNames.index(characterRace.lower())
    # Base stats start at 8 for each attribute
    base_stats = {
        "str": 8, "con": 8, "dex": 8,
        "int": 8, "wis": 8, "char": 8
    }
    # Apply racial stat bonuses to base stats
    base_stats["str"] += raceStrBonus[raceIndex]
    base_stats["con"] += raceConBonus[raceIndex]
    base_stats["dex"] += raceDexBonus[raceIndex]
    base_stats["int"] += raceIntBonus[raceIndex]
    base_stats["wis"] += raceWisBonus[raceIndex]
    base_stats["char"] += raceCharBonus[raceIndex]
    currentPoints = 27
    stats = base_stats.copy()

    # Randomize the stats
    if randomSelected:
        print("Randomizing stat distribution...")
        remaining = 27
        while remaining > 0:
            key = random.choice(list(stats.keys()))
            cost = 1 if stats[key] < 20 else 2
            if remaining >= cost:
                stats[key] += 1
                remaining -= cost
        print("Stats randomly assigned.")

    def printStats():
        print("\nCurrent Stats:")
        for key in stats:
            print(f"{key.upper()}: {stats[key]}")
        print("Points left:", currentPoints)

    # Don't randomize stats
    if randomSelected == False:
        print("You will now assign your stats. All stats start at 8 with racial bonuses applied.")
        print("You have 27 points to spend. Minimum value is 4. Values above 20 cost 2 per point.")
        while True:
            printStats()
            if all(val >= 4 for val in stats.values()):
                choice = input("Modify which stat? (str/con/dex/int/wis/char or 'done'): ").lower()
            else:
                choice = input("Modify which stat? (str/con/dex/int/wis/char): ").lower()
            if choice == "done":
                if not all(val >= 4 for val in stats.values()):
                    print("All stats must be at least 4 before finishing.")
                    continue
                if currentPoints > 0:
                    print("You must spend all stat points before finishing.")
                    continue
                break
            if choice not in stats:
                print("Invalid stat.")
                continue
            try:
                change = int(input(f"Change {choice.upper()} by how much? (+/-): "))
            except ValueError:
                print("Enter a number.")
                continue
            new_val = stats[choice] + change
            if new_val < 4:
                print("Stat cannot go below 4.")
                continue
            # Calculate point cost or refund for the change
            cost = 0
            if change > 0:
                for i in range(stats[choice] + 1, new_val + 1):
                    cost += 1 if i <= 20 else 2
            elif change < 0:
                for i in range(stats[choice], new_val, -1):
                    cost -= 1 if i <= 20 else 2
            if currentPoints - cost < 0:
                print("Not enough points.")
                continue
            stats[choice] = new_val
            currentPoints -= cost
    # Save finalized stats to global character stats
    characterStr = stats["str"]
    characterCon = stats["con"]
    characterDex = stats["dex"]
    characterInt = stats["int"]
    characterWis = stats["wis"]
    characterChar = stats["char"]
    print("\nFinal Stats:")
    printStats()
    # Affinity Assignment (allocate 10 points based on race's base affinities)
    affinityPoints = 10
    affinities = {
        "fire": raceFireAffinity[raceIndex],
        "earth": raceEarthAffinity[raceIndex],
        "water": raceWaterAffinity[raceIndex],
        "air": raceAirAffinity[raceIndex],
        "craft": raceCraftAffinity[raceIndex],
        "creation": raceCreateAffinity[raceIndex],
        "physical": racePhysicalAffinity[raceIndex],
        "utility": raceUtilityAffinity[raceIndex],
        "generic": raceGenericAffinity[raceIndex]
    }

    def printAffinities():
        print("\nCurrent Affinities:")
        for k in affinities:
            print(f"{k.capitalize()}: {affinities[k]}")
        print("Affinity points left:", affinityPoints)

    # Randomly assin affinities
    if randomSelected:
        print("\nRandomizing affinity points...")
        remaining = 10
        keys = list(affinities.keys())
        while remaining > 0:
            key = random.choice(keys)
            affinities[key] += 1
            remaining -= 1
        print("Affinities randomly assigned.")
    else:
        print("\nNow assign 10 affinity points based on your race's base affinities.")

    # Don't randomize affinity
    if randomSelected == False:
        while True:
            printAffinities()
            if affinityPoints == 0:
                choice = input("All points spent. Type 'done' to finish or continue editing: ").lower()
                if choice == "done":
                    break
            else:
                choice = input("Which affinity to modify? (or 'done'): ").lower()
                if choice == "done":
                    print("You must spend all affinity points before finishing.")
                    continue
            if choice not in affinities:
                print("Invalid affinity.")
                continue
            try:
                amt = int(input("Add how many points?: "))
            except ValueError:
                print("Enter a number.")
                continue
            if amt < 0 or amt > affinityPoints:
                print("Invalid amount.")
                continue
            affinities[choice] += amt
            affinityPoints -= amt
    # Save finalized affinities to global variables
    characterAffinityFire = affinities["fire"]
    characterAffinityEarth = affinities["earth"]
    characterAffinityWater = affinities["water"]
    characterAffinityAir = affinities["air"]
    characterAffinityCraft = affinities["craft"]
    characterAffinityCreation = affinities["creation"]
    characterAffinityPhysical = affinities["physical"]
    characterAffinityUtility = affinities["utility"]
    characterAffinityGeneric = affinities["generic"]
    print("\nFinal Affinities:")
    printAffinities()
    print("|")
    finalizeCombatStats()

def finalizeCombatStats():
    global characterInitiative, characterAc, characterSpeed
    global characterDex, characterRace
    raceIndex = raceNames.index(characterRace.lower())
    # Calculate Dexterity modifier (Dex - 10) // 2
    dex_mod = (characterDex - 10) // 2
    characterInitiative = dex_mod
    characterAc = 10 + dex_mod
    characterSpeed = raceSpeed[raceIndex]
    print("\nFinal Combat Stats:")
    print("Initiative:", characterInitiative)
    print("AC:", characterAc)
    print("Speed:", characterSpeed)
    saveCharacter()

def raceSelector():
    global characterRace
    global randomSelected
    print("|")
    print(raceNames)
    print("|")
    if randomSelected == False:
        print("Would you like to view a specific race? [0 = Yes  |  1 = No]")
        choice = input()
    else:
        choice = str("1")
        print("Ignoring question for randomness")
    if choice == "0" or choice == "Yes" or choice == "yes":
        print("|")
        print("Please type the name of the race you would like to view")
        print("|")
        choice = input()
        if choice.lower() in raceNames:
            raceIndex = raceNames.index(choice)
            print('You have selected', choice)
            print("|")
            print(choice, " has a size of ", raceSize[raceIndex])
            print("Speed: ", raceSpeed[raceIndex])
            if raceFlyingSpeed[raceIndex] != 0:
                print("Flying Speed: ", raceFlyingSpeed[raceIndex])
            if raceSwimSpeed[raceIndex] != 0:
                print("Swimming Speed: ", raceSwimSpeed[raceIndex])
            racialStatsBonuses(raceIndex, choice)
            print("This concludes all information about this race")
            print("Press ENTER to go back")
            input()
        else:
            print("That is not a valid input")
        raceSelector()  # Go back to race selection after viewing info
    elif choice == "1" or choice == "No" or choice == "no":
        print("Please select a race [just type its name (ensure it is spelled right)]")
        if randomSelected == False:
            choice = input()
        else:
            choice = random.choice(raceNames)
            print(choice, " has been selected")
        if choice in raceNames:
            raceIndex = raceNames.index(choice)
            print("You have selected", raceNames[raceIndex])
            print("Is this correct? [0 = Yes  |  1 = No  (Default is yes)]")
            if randomSelected == False:
                choice = input()
            else:
                choice = "0"
            if choice == "0" or choice == "Yes" or choice == "yes":
                print("Great! Moving on.")
                characterRace = raceNames[raceIndex]
                buildCharacter()
            elif choice == "1" or choice == "No" or choice == "no":
                print("Understood, restarting section...")
                raceSelector()
            else:
                print("Assuming yes..")
                characterRace = raceNames[raceIndex]
                buildCharacter()
        else:
            print("That is not a valid input")
            raceSelector()
    else:
        print("That is not a valid input")
        raceSelector()

def createCharacter():
    global characterName
    global randomSelected
    global first_names
    global last_names
    print("Would you like to generate a random character or make one manually? [0 = Random  |  1 = Manual]")
    choice = input()
    time.sleep(0.5)
    randomSelected = False
    if choice == "0" or choice == "Random" or choice == "random":
        print("Randomizing Character...")
        randomSelected = True
        characterName = random.choice(first_names) + " " + random.choice(last_names)
        raceSelector()
    elif choice == "1" or choice == "Manual" or choice == "manual":
        print("Please enter your character's name:")
        characterName = input()
        print("Next, choose your race...")
        raceSelector()
    else:
        print("That is not a valid input")
        createCharacter()

def manageCharacter():
    listSavedCharacters()
    loadCharacter()
    print("Work in progress...")

# Start the program
firstTime()
