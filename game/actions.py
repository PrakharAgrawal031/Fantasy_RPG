def explore(character):
    print(f"{character.name} explores the area... (nothing happens yet)")

def rest(character):
    print(f"{character.name} rests and recovers some health.")
    character.current_hp = min(character.current_hp + 5, character.max_hp)
    print(f"HP: {character.current_hp} / {character.max_hp}")