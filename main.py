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
            with open("data/rooms.json") as room_file:
                rooms = json.load(room_file)
                while True:
                    display_game_menu()

                    game_choice = input("Select: ")

                    if game_choice == "1":
                        current_room = rooms[player["current_room"]]
                        if current_room["zone_type"] == "green":
                            print("There are no enemies here.")
                            input("Press Enter to continue...")
                            clear_terminal()
                        else:
                            start_combat(player, enemy, current_room["zone_type"])
                    elif game_choice == "2":
                        display_equipment(player)
                    elif game_choice == "3":
                        move(player)
                    elif game_choice == "4":
                        break
            
        elif play_choice == "2":
            pass

    elif result == '2':
        pass

    elif result == '3':
        sys.exit()


if __name__ == "__main__":
    main()