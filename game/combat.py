import random

def combat(player, enemy):

    print(f"A wild {enemy.name} appears!")

    while player.current_hp > 0 and enemy.current_hp >0:
        print(f"\n{player.name} (HP: {player.current_hp}/{player.max_hp})")
        print(f"{enemy.name} (HP: {enemy.current_hp}/{enemy.max_hp})")

        print("Choose your action: ")
        print("1. Attack")
        print("2. Run")

        choice = input("> ")

        if choice == "1":
            dmg = player.stats['strength'] + random.randint(1,6) + player.damage_modifier
            enemy.current_hp -= dmg
            print(f"You strike {enemy.name} doing {dmg} damage.")
        
        elif choice == "2":
            if random.random() <0.5:
                print("You managed to escape.")
                return
            else:
                print("You failed to escape.")
        

        if enemy.is_alive():
            enemy_dmg = enemy.attack()
            player.current_hp -= enemy_dmg + player.defense_modifier
            print(f"The {enemy.name} hits you for {enemy_dmg + player.defense_modifier} damage!")
        

    if player.current_hp <= 0:
        print("\nYou were defeated...")
    else:
        print(f"\nYou defeated the {enemy.name}!")
        player.gain_exp(enemy.xp_reward)
        player.gain_gold(enemy.gold_reward)
        print(f"You gain {enemy.xp_reward} XP and {enemy.gold_reward} gold.")
        