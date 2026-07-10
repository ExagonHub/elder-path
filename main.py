import json
import sys
from game.combat import start_combat
from game.character import create_character
from game.ui import show_status
from game.ui import display_main_menu
from game.ui import display_play_menu
from game.ui import display_game_menu
from game.ui import display_equipment
from game.world import move
from game.ui import clear_terminal
from game.ui import display_more_menu
from game.ui import display_npc_list
from game.npc import talk_to_npc
from game.ui import display_equipment_menu
from game.items import item_action
from game.world import get_location
import random

def menu():
    display_main_menu()

    while True:
        choice = input('Enter your choice: ').strip()

        if choice in ['1','2','3']:
            return choice
        else:
            print('Invalid choice. Please enter 1, 2 or 3.')

def play_menu():
    
    while True:
        display_play_menu()

        game_choice = input("Select: ")

        if game_choice in ["1","2"]:
            return game_choice
        else:
            print("Invalid choice. Please enter 1 or 2")

def main():
    result = menu()

    if result == '1':
        play_choice = play_menu()

        if play_choice == "1":
            player = create_character()
            clear_terminal()
            print(f"\nWelcome, {player["name"]} the {player["class"]}!")
            print(f"Your journey begins in Ember's Cross...")
            input("\nPress Enter to continue...")
            clear_terminal()
            # show_status(player)
            with open("data/enemies.json") as file:
                enemies = json.load(file)
                enemy = enemies["ENEMY_001"]
            with open("data/npcs.json") as npc_file:
                npcs = json.load(npc_file)
            while True:
                show_status(player)
                display_game_menu()

                game_choice = input("Select: ")

                if game_choice == "1":
                    current_room = get_location(player)
                    if current_room["zone_type"] == "green":
                        print("There are no enemies here.")
                        input("\nPress Enter to continue...")
                        clear_terminal()
                    elif current_room.get("fixed_enemy"):
                        with open("data/enemies.json") as file:
                            enemy = json.load(file)[current_room]["fixed_enemy"]
                        start_combat(player, enemy, current_room["zone_type"])
                    elif current_room["enemy_pool"]:
                        enemy_key = random.choice(current_room["enemy_pool"])
                        with open("data/enemies.json") as file:
                            enemy = json.load(file)[enemy_key]
                        start_combat(player, enemy, current_room["zone_type"])
                    else:
                        print("There are no enemies here.")
                        input("\nPress Enter to continue...")
                        clear_terminal()

                elif game_choice == "2":
                    display_equipment(player)
                    eq_choice = display_equipment_menu()
                    if eq_choice =="1":
                        item_action(player)
                    elif eq_choice == "2":
                        pass
                    elif eq_choice == "3":
                        pass
                elif game_choice == "3":
                    move(player)
                elif game_choice == "4":
                    more_choice = display_more_menu(player)
                    current_room = get_location(player)
                    if current_room["zone_type"] == "green":
                        if more_choice == "1":
                            npc_choice, current_npcs = display_npc_list(npcs, player)
                            if npc_choice != str(len(current_npcs) + 1):
                                selected_npc = current_npcs[int(npc_choice) - 1]
                                talk_to_npc(player, selected_npc)
                        elif more_choice == "2":
                            break
                        elif more_choice == "3":
                            pass
                    else:
                        if more_choice == "1":
                            break
                        elif more_choice == "2":
                            pass

                else:
                    print("Invalid choice. Please enter 1, 2, 3 or 4.")
                    input("\nPlease Enter to continue...")
                    clear_terminal()
            
        elif play_choice == "2":
            pass

    elif result == '2':
        pass

    elif result == '3':
        sys.exit()


if __name__ == "__main__":
    main()