import random
import json
from game.character import Enemy
from game.combat import combat


def explore(character):
    safe_events = [
        "You wander through the forest and hear birds chirping.",
        "You stumble upon an abandoned campfire, still warm.",
        "You notice an ancient tree with carvings.",
        "A gentle stream flows nearby.",
    ]

    dangerous_events = [
        "You hear growls in the shadows.",
        "A rustling in the bushes catches your attention.",
        "You step on a loose branch and attract attention.",
        "You enter a dark cave that smells of danger.",
    ]

    # Decide if safe or dangerous event occurs
    if random.random() < 0.4:
        event = random.choice(safe_events)
        print("\n" + event)

        # Chance for loot
        if random.random() < 0.3:
            with open("data/items.json") as f:
                items = json.load(f)
            possible_loot = [item for item in items if random.random() < item.get("drop_rate", 1.0)]
            if possible_loot:
                loot = random.choice(possible_loot)
                loot_name = loot["name"]
                if loot_name.lower() == "gold":
                    character.gain_gold(loot.get("amount", 1))
                else:
                    character.add_item(loot_name, 1)
                    print(f"You found {loot_name}!")
            else:
                print("Nothing valuable found...")

    else:
        event = random.choice(dangerous_events)
        print("\n" + event)

        # High chance of enemy encounter
        if random.random() < 0.8:
            with open("data/enemies.json") as f:
                enemies = json.load(f)
            enemy_data = random.choice(enemies)
            enemy = Enemy(
                name=enemy_data["name"],
                stat=enemy_data["stat"],
                hp=enemy_data["hp"],
                xp_reward=enemy_data["xp_reward"],
                gold_reward=enemy_data["gold_reward"],
            )
            combat(character, enemy)
        else:
            print("\nThe road is quiet... nothing happens.")

def rest(character):
    heal_amount = min(5, character.max_hp - character.current_hp)
    if heal_amount > 0:
        character.current_hp += heal_amount
        print(f"\n{character.name} rests and recovers {heal_amount} HP.")
    else:
        print("You are already at full health.")
    
    #TODO: Might add risk of ambush in future.



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


# def use_item(character, item_name):
#     with open("data/items.json") as f:
#         items = json.load(f)

#     consumables = {i["name"]: i for i in items if i["type"] == "consumable"}
#     available = {name: qty for name, qty in character.inventory.items() if name in consumables}

#     if not available:
#         print("\nYou have no consumable items.")
#         return

#     print("\nConsumables in your Inventory:")
#     for i, (item, qty) in enumerate(available.items(), 1):
#         print(f"{i}. {item} (x{qty})")

#     choice = input("Choose an item to use (number or name): ").strip()

#     # Allow both number and name input
#     if choice.isdigit():
#         index = int(choice) - 1
#         if index < 0 or index >= len(available):
#             print("Invalid choice.")
#             return
#         item_name = list(available.keys())[index]
#     else:
#         item_name = choice.title()
#         if item_name not in available:
#             print("That consumable is not in your inventory.")
#             return

#     item_data = consumables[item_name]

#     print(f"\nYou used {item_name}.")
#     apply_effects(character, item_data.get("effects", {}))

#     character.remove_item(item_name, 1)
