import json
from rich.columns import Columns
from game.ui import display_level_up
from game.ui import display_class_menu

def create_character():
    while True:

        character_name = input("Enter your avatar's name: ").strip()

        if character_name == "":
            print("Please enter your avatar's name")

        elif not character_name.isalnum():
            print("Please use only letters and numbers. No spaces or special characters.")

        else:
            break

    while True:
        display_class_menu()

        class_choice = input("Choose your class: ")

        if class_choice in ["1","2","3"]:
            break
        
        else:
            print("Invalid choice. Please enter 1, 2 or 3")

    
    with open("data/classes.json") as file:
        classes = json.load(file)

    class_map = {"1": "Warrior", "2": "Assassin", "3": "Mage"}

    class_name = class_map[class_choice]

    class_stats = classes[class_name]

    player = {
        "name": character_name,
        "class": class_name,
        "level": 1,
        "xp": 0,
        "xp_to_next_level": 90,
        "max_hp": class_stats["hp"],
        "hp": class_stats["hp"],
        "max_mp": class_stats["mp"],
        "mp": class_stats["mp"],
        "base_damage": class_stats["base_damage"],
        "str": class_stats["str"],
        "dex": class_stats["dex"],
        "int": class_stats["int"],
        "vit": class_stats["vit"],
        "inventory": [None] * 18 ,
        "gold": 0
    }

    return player
            

def level_up(player):
    if player["xp"] >= player["xp_to_next_level"]:
        player["hp"] += 10
        player["max_hp"] += 10
        player["mp"] += 5
        player["max_mp"] += 5
        player["level"] += 1
        display_level_up(player)
        player["xp_to_next_level"] += 50


        attempts = 3

        while attempts > 0:
            print("Upgrade your stats\n")
            print("1 - STR")
            print("2 - DEX")
            print("3 - INT")
            print("4 - VIT")

            stat_choice = input("Select your stat: ")

            if stat_choice in ["1","2","3","4"]:
                if stat_choice == "1":
                    player["str"] += 1
                    attempts -= 1
                    
                elif stat_choice == "2":
                    player["dex"] += 1
                    attempts -= 1

                elif stat_choice == "3":
                    player["int"] += 1
                    attempts -= 1

                elif stat_choice == "4":
                    player["vit"] += 1
                    attempts -= 1

                else:
                    print("Invalid choice. Please enter 1, 2, 3 or 4.")