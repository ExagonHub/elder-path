import json
import random
from game.ui import display_room
from game.ui import clear_terminal

with open("data/rooms.json") as file:
    rooms = json.load(file)

def move(player):
    location = rooms[player["current_room"]]

    direction = input("Select your way (N/S/E/W): ").upper()

    direction_map = {
            "N": "north",
            "S": "south",
            "E": "east",
            "W": "west"
        }

    if direction in direction_map:

        full_direction = direction_map[direction]

        if full_direction in location["connections"]:
            player["previous_room"] = player["current_room"]
            player["current_room"] = location["connections"][full_direction]
            clear_terminal()
            display_room(rooms[player["current_room"]])
            encounter(player)
        else:
            print("No path in direction.")
            input("\nPress Enter to continue...")
            clear_terminal()
    else:
        print("Invalid direction.")

def encounter(player):
    from game.combat import start_combat
    location = rooms[player["current_room"]]

    if random.randint(1,100) <= location["encounter_chance"]:
        if location["zone_type"] == "yellow":
                enemy_key = random.choice(location["enemy_pool"])
                with open("data/enemies.json") as file:
                    enemy = json.load(file)[enemy_key]
                print(f"A {enemy['name']} appears!")
                while True:
                    print("1 - Fight")
                    print("2 - Flee")

                    choice = input("Are you a man or a coward: ")

                    if choice == "1":
                            start_combat(player, enemy, location["zone_type"])
                            if location["chest"] is not None and location["chest"]["opened"] == False:
                                print("A chest appears!")
                                open_chest(player, location)
                            break

                    elif choice == "2":
                        player["current_room"] = player["previous_room"]
                        print("Damn, so this is your decision what a shame..")
                        if player["previous_room"] is not None:
                            display_room(rooms[player["current_room"]])
                        break

                    else:
                        print("Invalid choice.")

        elif location["zone_type"] == "red":
            enemy_key = random.choice(location["enemy_pool"])
            with open("data/enemies.json") as file:
                enemy = json.load(file)[enemy_key]
                input("\nPress Enter to enter the dungeon...")
                clear_terminal()
                start_combat(player, enemy, location["zone_type"])

                if location["chest"] is not None and location["chest"]["opened"] == False:
                    print("A chest appears!")
                    open_chest(player, location)

def death_penalty(player):
    location = rooms[player["current_room"]]

    if location["zone_type"] == "yellow":
        player["hp"] = player["max_hp"] * 0.4
        player["mp"] = player["max_mp"] * 0.3

    elif location["zone_type"] == "red":
        player["gold"] -= int(player["gold"] * 0.3)
        print(f"You lost {int(player['gold'] * 0.3)} gold.")


def open_chest(player, location):
    while True:
        print("1 - Open")
        print("2 - Leave")

        choice = input("What do you do: ")

        if choice == "1":
            with open("data/weapons.json") as file:
                weapons = json.load(file)

            with open("data/armors.json") as file:
                armors = json.load(file)

                loots = {**weapons, **armors}

                for i, item_key in enumerate(location["chest"]["loot_pool"]):
                    print(f"{i + 1} - {loots[item_key]["name"]} ({loots[item_key]['quality']})")

                item_choice = input("Select item: ")

                selected_key = location["chest"]["loot_pool"][int(item_choice) - 1]

                selected_item = loots[selected_key]

                for i, slot in enumerate(player["inventory"]):
                    if slot is None:
                        player["inventory"][i] = selected_item
                        break
                
                location["chest"]["opened"] = True
                input("\nYou took the loot. Press Enter to continue...")
                clear_terminal()
                break

        elif choice == "2":
            input("\nNo need for it then. Press Enter to continue...")
            clear_terminal()
            break