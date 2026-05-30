import random
import json

def show_inventory(player):
    for i, item in enumerate(player["inventory"]):
        if item:
            print(f"{i+1}. {item["name"]}")
        else:
            print(f"{i+1}. Empty")


def select_item(player):
    while True:
        show_inventory(player)
        slot_choice = input("Select a slot: ")
        try:
            slot = int(slot_choice)
            if 1 <= slot <= 18 and player["inventory"][slot - 1] is not None:
                return slot - 1, player["inventory"][slot - 1]
            else:
                print("Invalid slot or empty. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def use_item(player, index, item):
    if item["effect"] == "heal":
        player["hp"] = min(player["hp"] + item["value"], player["max_hp"])
        player["inventory"][index] = None
        print(f"You used {item["name"]} and restored {item["value"]} HP.")


def drop_item(player, index):
    player["inventory"][index] = None



def item_action(player):
    index, item = select_item(player)

    while True:
        print("1 - Use")
        print("2 - Drop")

        action_choice = input("Select action: ")

        if action_choice in ["1","2"]:
            if action_choice == "1":
                use_item()
            elif action_choice == "2":
                drop_item()
        else:
            print("Invalid choice. Please enter 1 or 2.")


def enemy_drop(player, enemy):
    roll = random.random()
    if roll < 0.33:
        item_id = enemy["drop"]
        with open("data/items.json") as file:
            items = json.load(file)
            item = items[item_id]
            for i, slot in enumerate(player["inventory"]):
                if slot is None:
                    player["inventory"][i] = item
                    print(f"{enemy['name']} dropped [{item["quality"]}] {item["name"]}!")
                    break

    gold_roll = random.random()
    if gold_roll < 0.65:
        gold = random.randint(enemy["gold_min"], enemy["gold_max"])
        player["gold"] += gold
        print(f"You found {gold} gold!")