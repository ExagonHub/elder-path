import json

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
        print("1 - Warrior")
        print("2 - Assassin")
        print("3 - Mage")

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
        "hp": class_stats["hp"],
        "mp": class_stats["mp"],
        "base_damage": class_stats["base_damage"],
        "str": class_stats["str"],
        "dex": class_stats["dex"],
        "int": class_stats["int"],
        "vit": class_stats["vit"]
    }

    return player
            

def level_up(player):
    if player["xp"] >= player["xp_to_next_level"]:
        player["hp"] += 10
        player["mp"] += 5
        player["level"] += 1
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