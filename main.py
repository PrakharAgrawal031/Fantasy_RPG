# main.py
import sys
from game.character import Character
from game.actions import explore, rest

RACES = ["Human", "Dwarf", "Elf", "Orc"]
CLASSES = ["Warrior", "Mage", "Rogue", "Cleric"]
STATS = ["strength", "dexterity", "intelligence", "charisma", "endurance", "constitution"]

def main_menu():
    while True:
        print("Welcome to Chat RPG!")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            return new_game()
        elif choice == '2':
            return load_game()
        elif choice == '3':
            print("Exiting game. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
    


def new_game():
    print("\nStarting a new game...")
    print("\n==== Character Creation ====")
    
    #get name
    name = input("Enter your character's name: ").strip()
    
    #get valid race
    while True:
        race = input(f"Choose your race ({','.join(RACES)}): ").strip().capitalize()

        if race in RACES:
            break
        else:
            print("Invalid choice. Please choose a valid option.")

    #get valid class
    while True:
        char_class = input(f"Choose your class ({','.join(CLASSES)}): ").strip().capitalize()

        if char_class in CLASSES:
            break
        else:
            print("Invalid choice. Please choose a valid option.")

    #Manual stat allocation

    total_points = 30
    min_stat = 3

    stats = {stat: min_stat for stat in STATS}
    remaining_points = total_points - min_stat * len(STATS)

    print(f"\nYou have {total_points} points to distribute among the following stats: {', '.join(STATS)}")
    print(f"Each stat must have at least {min_stat} points. You have {remaining_points} points remaining to allocate.")

    for stat in STATS:
        while remaining_points > 0:
            try:
                print(f"\nRemaining points: {remaining_points}")

                val = int(input(f"Assign point to {stat} (current: {stats[stat]}): "))

                if val < 0 or val > remaining_points:
                    print(f"Invalid input. You can assign between 0 and {remaining_points} points.")
                    continue

                stats[stat] += val
                remaining_points -= val
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    print("\nFinal stats: ", stats)

    character = Character(name, race, char_class, stats=stats)

    # #Generating stats randomly for now. Will modify later to allow user input
    # character = Character(name, race, char_class)

    print("\nCharacter created successfully!")
    print(character)

    #save character
    character.save()
    print("Character created and saved successfully!\n")
    return character


def load_game():
    try:
        character = Character.load()
        print("\nCharacter loaded successfully!")
        print(character)
        return character

        #TODO: Add game loop here
    except FileNotFoundError:
        print("No saved game found. Please start a new game first.\n")




#add basic game loop

def game_loop(character):
    
    print(f"\nWelcome to the adventure, {character.name} the {character.race} {character.char_class}!\n")

    while True:
        print("\n--- Main menu ---")
        print("1. Explore")
        print("2. View character info")
        print("3. Rest")
        print("4. Save & Quit")

        choice = input("Choose an action: ").strip()

        if choice == "1":
            explore(character)
        elif choice == "2":
            print('\n')
            print(character)
        elif choice == "3":
            rest(character)
        elif choice == "4":
            character.save()
            print("Progress saved. Goodbye Adventurer!")
            break 
        else:
            print("Invalid choice. Try again.")


    # stats = {
    #     'strength': 10,
    #     'dexterity': 10,
    #     'intelligence': 10,
    #     'constitution': 10,
    #     'charisma': 10,
    #     'endurance': 10
    # }

if __name__ == "__main__":
    character = main_menu()
    if character:
        game_loop(character)
