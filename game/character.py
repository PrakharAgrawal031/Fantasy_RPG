import json
import os
import random
import math


# character.py

def apply_effects(character, effects):
    """Apply effects from a consumable item dynamically."""
    for effect, value in effects.items():
        if effect == "heal":
            healed = min(value, character.max_hp - character.current_hp)
            character.current_hp += healed
            print(f"You recover {healed} HP.")
        elif effect == "mana_restore":
            # Placeholder until mana system is implemented
            print(f"You restore {value} Mana.")
        elif effect == "gold":
            character.gain_gold(value)
            print(f"You gained {value} gold.")
        else:
            print(f"Effect '{effect}' is not implemented yet.")


class Character:
    def __init__(self, name, race, char_class, stats=None, level=1, xp = 0, inventory=None):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.stats = stats if stats else self.generate_stats()
        self.inventory = inventory if inventory else {"gold": 0}
        self.equipment = {
            "right_hand": None,
            "left_hand": None,
            "head": None,
            "body": None,
            "feet": None,
            "accessory": None
        }
        self.xp = xp
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
        
        return stats

    def calculate_max_hp(self):
        return self.stats['constitution'] * 5 + self.stats['endurance'] * 2 + self.level * 3
    
    def next_exp_threshold(self):
        base = 100
        growth = 1.5
        return math.floor(base * (self.level ** growth))
    
    def gain_exp(self, amount):
        self.xp += amount
        print(f" Gained {amount} xp! Total xp: {self.xp}")
        while self.xp >= self.next_exp_threshold():
            self.level_up()

    
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
        
        old_max_hp = self.max_hp
        self.max_hp = self.calculate_max_hp()
        self.current_hp += (self.max_hp - old_max_hp)  # Increase current HP


    # ---- Inventory Management ----

    @property
    
    def carry_capacity(self):
        return 10 + (self.stats["strength"]*2) 
    
    @property
    def current_weight(self):
        with open("data/items.json") as f:
            items = json.load(f)
        total = 0
        for item_name, qty in self.inventory.items():
            if item_name.lower() == "gold":
                continue  # gold has no weight
            item_data = next((i for i in items if i["name"] == item_name), None)
            if item_data:
                total += item_data.get("weight", 1) * qty
        return total
    
    def can_carry(self, item_name, qty=1):
        with open("data/items.json") as f:
            items = json.load(f)
        item_data = next((i for i in items if i["name"] == item_name), None)
        if not item_data:
            return False
        new_weight = self.current_weight + item_data.get("weight", 1) * qty
        return new_weight <= self.carry_capacity

    def gain_gold(self, amount):
        self.inventory["gold"] = self.inventory.get("gold", 0) + amount
        print(f"Gained {amount} gold! Total gold: {self.inventory['gold']}")
        

    def add_item(self, item_name, qty=1):

        if not self.can_carry(item_name, qty):
            print(f"⚠️ Cannot carry {item_name}, too heavy!")
            return False

        self.inventory[item_name] = self.inventory.get(item_name, 0) + qty
        print(f"Added {qty}x {item_name} to inventory.")
        return True


    def remove_item(self, item_name, qty = 1):
        if self.inventory.get(item_name, 0) >= qty:
            self.inventory[item_name] -= qty
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]
            print(f"Removed {qty}x {item_name} from inventory.")
            return True
        print(f"⚠️ You don’t have enough {item_name}.")
        return False

    
    # ----- Equipment System -----

    def equip_item(self, item_name):
        # Equip an item if possible
        with open("data/items.json") as f:
            items = json.load(f)
        item_data = next((i for i in items if i["name"] == item_name), None)

        if not item_data:
            print(f"⚠️ Item {item_name} not found in items.json")
            return False

        if item_name not in self.inventory:
            print(f"⚠️ You don’t have {item_name} in inventory.")
            return False

        slot = item_data.get("slot")
        if not slot:
            print(f"⚠️ {item_name} cannot be equipped.")
            return False

        # Unequip existing item in slot
        if self.equipment.get(slot):
            print(f"Unequipped {self.equipment[slot]}")
            self.add_item(self.equipment[slot])

        # Equip new item
        self.equipment[slot] = item_name
        self.remove_item(item_name, 1)
        print(f"Equipped {item_name} in {slot}.")
        return True



        # """Equip an item from inventory"""
        # if "slot" not in item:
        #     print(f"{item['name']} cannot be equipped.")
        #     return
    
        # slot = item['slot']
        # prev_item = self.equipment.get(slot)

        # if prev_item:
        #     self.damage_modifier -= prev_item.get("damage_modifier", 0)
        #     self.defense_modifier -= prev_item.get("defense_modifier", 0)
        #     self.inventory.append(prev_item["name"])
        #     print(f"Unequipped {prev_item['name']} from {slot}.")

        # self.equipment[slot] = item
        # self.damage_modifier += item.get("damage_modifier", 0)
        # self.defense_modifier += item.get("defense_modifier", 0)
        # if item["name"] in self.inventory:
        #     self.remove_item(item["name"])
        # print(f"Equipped {item['name']} in {slot}.")

    def unequip_item(self, slot):
        if slot not in self.equipment or not self.equipment[slot]:
            print(f"No item equipped in {slot}.")
            return False
        
        item_name = self.equipment[slot]
        self.equipment[slot] = None
        self.add_item(item_name)
        print(f"Unequipped {item_name} from {slot}.")
        return True
    

    def use_item(character, item_name):
        with open("data/items.json") as f:
            items = json.load(f)

        consumables = {i["name"]: i for i in items if i["type"] == "consumable"}
        available = {name: qty for name, qty in character.inventory.items() if name in consumables}

        if not available:
            print("\nYou have no consumable items.")
            return

        print("\nConsumables in your Inventory:")
        for i, (item, qty) in enumerate(available.items(), 1):
            print(f"{i}. {item} (x{qty})")

        choice = input("Choose an item to use (number or name): ").strip()

        # Allow both number and name input
        if choice.isdigit():
            index = int(choice) - 1
            if index < 0 or index >= len(available):
                print("Invalid choice.")
                return
            item_name = list(available.keys())[index]
        else:
            item_name = choice.title()
            if item_name not in available:
                print("That consumable is not in your inventory.")
                return

        item_data = consumables[item_name]

        print(f"\nYou used {item_name}.")
        apply_effects(character, item_data.get("effects", {}))

        character.remove_item(item_name, 1)
    
    # ----- Combat modifiers -----
    @property
    def damage_modifier(self):
        """Sum of all equipped items' damage modifiers"""
        with open("data/items.json") as f:
            items = json.load(f)
        dmg = 0
        for slot, item_name in self.equipment.items():
            if not item_name:
                continue
            item_data = next((i for i in items if i["name"] == item_name), None)
            if item_data:
                dmg += item_data.get("damage_modifier", 0)
        return dmg

    @property
    def defense_modifier(self):
        """Sum of all equipped items' defense modifiers"""
        with open("data/items.json") as f:
            items = json.load(f)
        defense = 0
        for slot, item_name in self.equipment.items():
            if not item_name:
                continue
            item_data = next((i for i in items if i["name"] == item_name), None)
            if item_data:
                defense += item_data.get("defense_modifier", 0)
        return defense
    

# ----- Save and Load game functions ----


    def save(self, filename='character.json'):

        os.makedirs("saves", exist_ok=True)
        filepath = os.path.join("saves", filename)

        data = {
            'name': self.name,
            'race': self.race,
            'char_class': self.char_class,
            'level': self.level,
            'xp': self.xp,
            'equipment': self.equipment,
            'stats': self.stats,
            'inventory': self.inventory,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
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
            inventory=data['inventory'],
            xp = data['xp'],
        )

        character.equipment = data.get('equipment')
        character.xp = data.get('xp', 0)
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
            f"Exp: {self.xp}/{self.next_exp_threshold()}\n"
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
    
