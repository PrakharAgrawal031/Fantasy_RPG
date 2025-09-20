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
    if random.random() < 0.6:
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