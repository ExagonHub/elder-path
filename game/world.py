import json
import random
from game.ui import display_room
from game.ui import clear_terminal

with open("data/rooms.json") as file:
    rooms = json.load(file)

with open("data/dungeons_index.json") as file:
    dungeons_index = json.load(file)

dungeon_cache = {}

def move(player):
    location = get_location(player)

    if location.get("fixed_enemy") and player["current_room"] not in (player.get("cleared_rooms") or []):
        print("\nYou must defeat what guard this place before you can move on.")
        input("\nPress Enter to continue...")
        clear_terminal()
        return

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
            destination = location["connections"][full_direction]

            if destination.startswith("DROOM_"):
                target_dungeon = player["current_dungeon"]
                destination_data = get_room_data(destination, target_dungeon)

                if destination_data.get("fixed_enemy"):
                    print("\nA powerful being awaits beyond this door.")
                    print("Once you enter, there is no turning back.")
                    confirm = input("Do you wish to proceed? (Y/N): ").upper()
                    if confirm != "Y":
                        print("You step back.")
                        input("\nPress Enter to continue...")
                        clear_terminal()
                        return


            if player["current_room"].startswith("DROOM_") and not destination.startswith("DROOM_"):
                player["current_dungeon"] = None

            player["previous_room"] = player["current_room"]
            player["current_room"] = destination
            clear_terminal()
            encounter(player)
            new_location = get_location(player)
            if new_location["zone_type"] == "green":
                player["last_safe_room"] = player["current_room"]

        elif full_direction == "north" and location.get("dungeon_entrance"):
            dungeon_id = location["dungeon_entrance"]
            entry_droom = dungeons_index[dungeon_id]["entry_droom"]

            player["current_dungeon"] = dungeon_id
            player["previous_dungeon"] = player["current_room"]
            player["current_room"] = entry_droom
            clear_terminal()
            input("\nPress Enter to enter the dungeon...")
            encounter(player)
            new_location = get_location(player)
            if new_location["zone_type"] == "green":
                player["last_safe_room"] = player["current_room"]

        else:
            print("No path in direction.")
            input("\nPress Enter to continue...")
            clear_terminal()



def encounter(player):
    from game.combat import start_combat
    location = get_location(player)
    

    if location.get("fixed_enemy"):
        if player["current_room"] in (player.get("cleared_rooms") or []):
            return
        enemy_id = location["fixed_enemy"]
        if enemy_id.startswith("BOSS_"):
            with open("data/bosses.json") as file:
                enemy = json.load(file)[enemy_id]
        else:
            with open("data/enemies.json") as file:
                enemy = json.load(file)[enemy_id]
        if enemy.get("dialogue"):
            from rich.console import Console
            console = Console()
            console.print(f"\n[bold red]{enemy['dialogue']}[/bold red]")
            input("\nPress Enter to continue...")
            clear_terminal()
        result = start_combat(player, enemy, location["zone_type"], is_fixed=True)
        if result == "victory":
            if location.get("chest") is not None and not location["chest"].get("opened"):
                open_chest(player, location)
        return

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
                            result = start_combat(player, enemy, location["zone_type"], is_fixed=False)
                            if result == "victory":
                                if location["chest"] is not None and not location["chest"]["opened"]:
                                    open_chest(player, location)
                            break


                    elif choice == "2":
                        player["current_room"] = player["previous_room"]
                        print("Damn, so this is your decision what a shame..")
                        if player["previous_room"] is not None:
                            display_room(get_location(player))
                        break

                    else:
                        print("Invalid choice.")

        elif location["zone_type"] == "red":
            enemy_key = random.choice(location["enemy_pool"])
            with open("data/enemies.json") as file:
                enemy = json.load(file)[enemy_key]
                clear_terminal()
                result = start_combat(player, enemy, location["zone_type"], is_fixed=False)

                if result == "victory":
                    if location["chest"] is not None and not location["chest"]["opened"]:
                        open_chest(player, location)

def death_penalty(player):
    location = get_location(player)

    if location["zone_type"] == "yellow":
        player["hp"] = player["max_hp"] * 0.4
        player["mp"] = player["max_mp"] * 0.3

    elif location["zone_type"] == "red":
        player["gold"] -= int(player["gold"] * 0.3)
        print(f"You lost {int(player['gold'] * 0.3)} gold.")
        player["hp"] = int(player["max_hp"] * 0.4)
        player["mp"] = int(player["max_mp"] * 0.3)

    player["current_room"] = player["last_safe_room"]
    player["current_dungeon"] = None


def open_chest(player, location):
    chest_type = location["chest"].get("type", "normal")

    if chest_type == "boss":
        print("\nA chest appears! The Hollow Sovereign's essence radiates from within.")
    elif chest_type == "gatekeeper":
        print("\nA chest appears! The Cursed Knight's weapons lay before you.")
    else:
        print("\nA chest appears!")
    while True:
        print("1 - Open")
        print("2 - Leave")

        choice = input("What do you do: ")

        if choice == "1":
            if chest_type == "boss":
                with open("data/items.json") as file:
                    items = json.load(file)
                for item_key in location["chest"]["loot_pool"]:
                    item = items[item_key]
                    for i, slot in enumerate(player["inventory"]):
                        if slot is None:
                            player["inventory"][i] = item
                            break

                player["gold"] += location["chest"]["gold"]
                print(f"\nYou obtained {item["name"]}!")
                print(f"\nYou obtained {location["chest"]["gold"]} gold!")
                location["chest"]["opened"] = True
                input("\nPress Enter to continue...")
                clear_terminal()
                break

            elif chest_type == "gatekeeper":
                with open("data/weapons.json") as file:
                    weapons = json.load(file)
                for i, item_key in enumerate(location["chest"]["loot_pool"]):
                    print(f"{i + 1} - {weapons[item_key]["name"]} ({weapons[item_key]['quality']})")
                item_choice = input("Select item: ")
                selected_key = location["chest"]["loot_pool"][int(item_choice) - 1]
                selected_item = weapons[selected_key]
                for i, slot in enumerate(player["inventory"]):
                    if slot is None:
                        player["inventory"][i] = selected_item
                        break
                player["gold"] += location["chest"]["gold"]
                print(f"\nYou obtained {selected_item["name"]}!")
                print(f"You obtained {location["chest"]["gold"]} gold!")
                location["chest"]["opened"] = True
                input("\nPress enter to continue...")
                clear_terminal()
                break

            else:
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

def get_dungeon_data(dungeon_id):
    if dungeon_id in dungeon_cache:
        return dungeon_cache[dungeon_id]
    
    file_name = dungeons_index[dungeon_id]["file"]
    with open(f"data/dungeons/{file_name}") as file:
        data = json.load(file)

    dungeon_cache[dungeon_id] = data
    return data

def get_location(player):
    room_id = player["current_room"]
    if room_id.startswith("DROOM_"):
        dungeon_id = player.get("current_dungeon")
        if dungeon_id is None:
            dungeon_id = "DUNGEON_001"
            player["current_dungeon"] = dungeon_id
        dungeon_data = get_dungeon_data(dungeon_id)
        return dungeon_data[room_id]
    else:
        return rooms[room_id]
    
def get_room_data(room_id, dungeon_id):
    if room_id.startswith("DROOM_"):
        return get_dungeon_data(dungeon_id)[room_id]
    else:
        return rooms[room_id]