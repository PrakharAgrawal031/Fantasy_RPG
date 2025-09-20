import json
import os
import random

class Character:
    def __init__(self, name, race, char_class, stats=None, level=1, inventory=None):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.stats = stats if stats else self.generate_stats()
        self.inventory = inventory if inventory else []

        self.max_hp = self.calculate_max_hp()
        self.current_hp = self.max_hp

    def generate_stats(self, total_point = 30, min_stat = 1, max_stat = 20):
        '''Generates character stats using a fix total point system.'''
        stats = ['strength', 'dexterity', 'intelligence', 'charisma', 'endurance', 'constitution']

        stats = {name: min_stat for name in stats}

        remaining_points = total_point - min_stat * len(stats)

        while remaining_points > 0:
            choice = random.choice(stats)
            if stats[choice] < max_stat:
                stats[choice] += 1
                remaining_points -= 1

        #applying race modifiers

        if self.race.lower() == 'elf':
            stats['dexterity'] = min(stats['dexterity']+2, max_stat)
            stats['intelligence'] = min(stats['dexterity']+2, max_stat)
        
        elif self.race.lower() == 'dwarf':
            stats['constitution'] = min(stats['constitution']+2, max_stat)
            stats['strength'] = max(stats['strength']+2, max_stat)
            stats['endurance'] = min(stats['endurance']+1, max_stat)

        elif self.race.lower() == "human":
            stats["charisma"] = min(stats["charisma"] + 1, max_stat)
            stats["constitution"] = min(stats["constitution"] + 1, max_stat)

        elif self.race.lower() == "orc":
            stats["strength"] = min(stats["strength"] + 2, max_stat)
            stats["endurance"] = min(stats["endurance"] + 1, max_stat)
            stats["intelligence"] = max(stats["intelligence"] - 1, min_stat)

        
        #applying class modifiers
        if self.char_class.lower() == 'warrior':
            stats['strength'] = min(stats['strength']+2, max_stat)
            stats['endurance'] = min(stats['endurance']+2, max_stat)
            stats['constitution'] = min(stats['constitution']+1, max_stat)
        
        elif self.char_class.lower() == 'mage':
            stats['intelligence'] = min(stats['intelligence']+3, max_stat)
        
        elif self.char_class.lower() == 'rogue':
            stats['dexterity'] = min(stats['dexterity']+2, max_stat)
            stats['charisma'] = min(stats['charisma']+1, max_stat)

        elif self.char_class.lower() == 'cleric': 
            stats['intelligence'] = min(stats['intelligence'] + 1, max_stat)
            stats['charisma'] = min(stats['charisma'] + 1, max_stat)
            stats['constitution'] = min(stats['constitution'] + 1, max_stat)

    def calculate_max_hp(self):
        return self.stats['constitution'] * 5 + self.stats['endurance'] * 2 + self.level * 3
    
    
    def level_up(self):
        self.level += 1
        print(f"\n You have reached level {self.level}!")

        print("You can increase your one of your stats by 2 points.")
        
        for i, stat in enumerate(self.stats.keys(), start = 1):
            print(f"{i}. {stat} (current: {self.stats[stat]})")

        while True:
            try: 
                choice = int(input("Enter the number of stat: "))
                stat_choice = list(self.stats.keys())[choice - 1]
            except(ValueError, IndexError):
                print("Invalid choice. Please try again.")
                continue

            if self.stats[stat_choice] >= 20:
                print(f"{stat_choice} is already at maximum value. Choose another stat.")
            
            else:
                self.stats[stat_choice] = min(self.stats[stat_choice] + 2, 20)
                print(f"{stat_choice} increased to {self.stats[stat_choice]}.")
                break


    def add_item(self, item):
        self.inventory.append(item)
        print(f"{item} added to inventory.")


    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item} removed from inventory.")
        else:
            print(f"{item} not found in inventory.")


    def save(self, filename='character.json'):

        os.makedirs("saves", exist_ok=True)
        filepath = os.path.join("saves", filename)

        data = {
            'name': self.name,
            'race': self.race,
            'char_class': self.char_class,
            'level': self.level,
            'stats': self.stats,
            'inventory': self.inventory,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Character saved.")

    
    @classmethod
    def load(cls, filename='character.json'):
        filepath = os.path.join("saves", filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No save file found at {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)

        character = cls(
            name=data['name'],
            race=data['race'],
            char_class=data['char_class'],
            stats=data['stats'],
            level=data['level'],
            inventory=data['inventory']
        )

        character.max_hp = data.get('max_hp', character.calculate_max_hp())
        character.current_hp = data.get('current_hp', character.max_hp)

        return character
    
    def __str__(self):
        return(
            f"Name: {self.name}\n"
            f"Race: {self.race}\n"
            f"Class: {self.char_class}\n"
            f"Level: {self.level}\n"
            f"HP: {self.current_hp}\n"
            f"Stats: {self.stats}\n"
            f"Inventory: {self.inventory}\n"
        )



# creating enemies
class Enemy:
    def __init__(self, name, stat, hp, xp_reward, gold_reward):
        self.name = name
        self.stat = stat
        self.max_hp = hp
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.current_hp = hp
    
    def is_alive(self):
        return self.current_hp>0
    
    def attack(self):
        return self.stat['strength'] + random.randint(1,4)
    
    def __str__(self):
        return f"{self.name} (HP: {self.current_hp}/{self.max_hp})"

