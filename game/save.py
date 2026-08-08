import json
import os

def save_game(player):
    os.makedirs("saves", exist_ok=True)
    player["save_version"] = "0.9.1"
    file_name = f"saves/{player['name']}.json"
    with open (file_name, "w") as file:
        json.dump(player, file, indent=4)
    print("Game Saved.")


def load_game():
    save_files = [f for f in os.listdir("saves") if f.endswith(".json")]

    if not save_files:
        print("No saved games found.")
        return None

    print("\nSaved Games: ")
    for i, save_file in enumerate(save_files):
        with open(f"saves/{save_file}") as file:
            save_data = json.load(file)
        print(f"{i + 1} - {save_data['name']} | {save_data['class']} | Level {save_data['level']} | {save_data['current_room']}")

        while True:
            print("\nL - Load | D - Delete | B - Back")
            action = input("Select: ").strip().upper()

            if action == "L":
                try:
                    choice = int(input("Select save file: "))
                    if 1 <= choice <= len(save_files):
                        with open(f"saves/{save_files[choice - 1]}") as file:
                            player = json.load(file)
                        print(f"\nWelcome back, {player["name"]}!")
                        return player
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a number.")

            elif action == "D":
                try:
                    choice = int(input("Select save to delete: "))
                    if 1 <= choice <= len(save_files):
                        confirm = input(f"Delete {save_files[choice - 1]}? (Y/N): ").strip().upper()
                        if confirm == "Y":
                            os.remove(f"saves/{save_files[choice - 1]}")
                            print("Save deleted.")
                            return None
                        else:
                            print("Cancelled.")
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a number.")

            elif action == "B":
                return None

            else:
                print("Invalid choice.")