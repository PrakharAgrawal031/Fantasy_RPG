import random
import json
from game.character import Enemy
from game.combat import combat


def explore(character):
    #Just a placeholder. To be modified later
    events = [
        "You wander through the forest and hear birds chirping.",
        "You stumble upon an abandoned campfire, still warm.",
        #"A merchant caravan passes by on the dusty road.",
        #"You find strange footprints leading deeper into the woods...",
    ]

    print("\n" + random.choice(events))
    
    if random.random()<0.6:
        with open("data\enemies.json") as f:
            enemies = json.load(f)

        enemy_data = random.choice(enemies)

        enemy = Enemy(
            name = enemy_data["name"],
            stat = enemy_data["stat"],
            hp = enemy_data["hp"],
            xp_reward = enemy_data["xp_reward"],
            gold_reward = enemy_data["gold_reward"],
        )
        
        combat(character, enemy)

    else:
        print("\nThe road is quiet... nothing happens.")

    #TODO: Add enemy encounter and item drops

def rest(character):
    heal_amount = min(5, character.max_hp - character.current_hp)
    if heal_amount > 0:
        character.current_hp += heal_amount
        print(f"\n{character.name} rests and recovers {heal_amount} HP.")
    else:
        print("You are already at full health.")
    
    #TODO: Might add risk of ambush in future.