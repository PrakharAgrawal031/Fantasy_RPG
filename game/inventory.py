import json

def get_item_data(item_name):
    with open("data/items.json") as f:
        items = json.load(f)
    return next((i for i in items if i["name"] == item_name), None)


def equipment_menu(character):
    while True:
        print("\n=== Equipment ===")
        for slot, item_name in character.equipment.items():
            if item_name:
                print(f"{slot.title()}: {item_name}")
            else:
                print(f"{slot.title()}: (empty)")

        print("\n1. Equip an item")
        print("2. Unequip an item")
        print("3. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            equip_item_from_inventory(character)
        elif choice == "2":
            unequip_item(character)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def equip_item_from_inventory(character):
    # Find equippable items in inventory
    equippables = []
    for item in character.inventory:
        item_data = get_item_data(item)
        if item_data and item_data.get("type") in ["weapon", "armor", "accessory"]:
            equippables.append(item)

    if not equippables:
        print("\nYou have no equippable items.")
        return

    print("\n=== Equippable Items ===")
    for i, item_name in enumerate(equippables, start=1):
        qty = character.inventory[item_name]
        print(f"{i}. {item_name} (x{qty})")

    choice = input("\nChoose an item to equip (number or name, or 'back'): ").strip()

    if choice.lower() == "back":
        return

    try:
        if choice.isdigit():
            item_name = equippables[int(choice) - 1]
        else:
            item_name = next(i for i in equippables if i.lower() == choice.lower())

        # Get slot type
        item_data = get_item_data(item_name)
        if not item_data or "slot" not in item_data:
            print(f"Error: {item_name} has no valid slot defined in items.json.")
            return

        slot = item_data["slot"]

        # If something is already equipped in that slot, unequip it first

        character.equip_item(item_name)
        print(f"You equipped {item_name} in {slot}.")

    except (IndexError, StopIteration):
        print("Invalid choice.")



def unequip_item(character):
    choice = input("\nEnter slot name to unequip (or 'back'): ").strip().lower()
    if choice in character.equipment and character.equipment[choice]:
        removed_item = character.equipment[choice]
        character.unequip_item(choice)
        print(f"You unequipped {removed_item}.")
    elif choice == "back":
        return
    else:
        print("Invalid choice or slot empty.")


def consumables_menu(character):
    consumables = [item for item in character.inventory if get_item_data(item)["type"] == "consumable"]

    if not consumables:
        print("\nYou have no consumables.")
        return

    print("\n=== Consumables ===")
    for i, item_name in enumerate(consumables, start=1):
        qty = character.inventory[item_name]
        print(f"{i}. {item_name} (x{qty})")

    choice = input("\nChoose an item to use (number or name, or 'back'): ").strip()

    if choice.lower() == "back":
        return

    try:
        if choice.isdigit():
            item_name = consumables[int(choice) - 1]
        else:
            item_name = next(i for i in consumables if i.lower() == choice.lower())

        character.use_item(item_name)
    except (IndexError, StopIteration):
        print("Invalid choice.")


def misc_items_menu(character):
    misc_items = [
        item for item in character.inventory
        if get_item_data(item)["type"] not in ["consumable", "weapon", "armor", "accessory"]
    ]

    if not misc_items:
        print("\nYou have no misc items.")
        return

    print("\n=== Misc Items ===")
    for i, item_name in enumerate(misc_items, start=1):
        qty = character.inventory[item_name]
        print(f"{i}. {item_name} (x{qty})")

    input("\nPress Enter to go back.")


def inventory_menu(character, only_consumables=False):
    while True:
        print("\n=== Inventory ===")
        if not character.inventory:
            print("Your inventory is empty.")
            break

        if only_consumables:
            consumables_menu(character)
            break

        print("1. Equipment")
        print("2. Consumables")
        print("3. Misc Items")
        print("4. Back to main menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            equipment_menu(character)
        elif choice == "2":
            consumables_menu(character)
        elif choice == "3":
            misc_items_menu(character)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
