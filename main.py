import json
import sys
from game.combat import start_combat
from game.character import create_character
from game.ui import show_status
from game.ui import display_main_menu
from game.ui import display_play_menu

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
            # show_status(player)
            with open("data/enemies.json") as file:
                enemies = json.load(file)
                enemy = enemies["ENEMY_001"]
            
            start_combat(player, enemy)
        elif play_choice == "2":
            pass

    elif result == '2':
        pass

    elif result == '3':
        sys.exit()


if __name__ == "__main__":
    main()