import random
import json
from game.ui import display_inventory
from game.equipment import equip_item
from game.ui import clear_terminal

def show_inventory(player):
    for i, item in enumerate(player["inventory"]):
        if item:
            print(f"{i+1}. {item["name"]}")
        else:
            print(f"{i+1}. Empty")


def select_item(player):
    while True:
        display_inventory(player)
        slot_choice = input("Select a slot (0 to exit): ")
        if slot_choice == "0":
            clear_terminal()
            return None, None
        try:
            slot = int(slot_choice)
            if 1 <= slot <= 18 and player["inventory"][slot - 1] is not None:
                return slot - 1, player["inventory"][slot - 1]
            else:
                print("Invalid slot or empty. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def use_item(player, index, item):
    if item["type"] in ["weapon", "armor", "accessory", "loot"]:
        print("This item cannot be used.")
        return

    if item["effect"] == "heal":
        player["hp"] = min(player["hp"] + item["value"], player["max_hp"])
        player["inventory"][index] = None
        print(f"You used {item["name"]} and restored {item["value"]} HP.")




def drop_item(player, index):
    player["inventory"][index] = None



def item_action(player):
    index, item = select_item(player)

    if index is None:
        return

    while True:
        if item["type"] in ["weapon", "armor", "accessory"]:
            print("1 - Equip")
            print("2 - Drop")
            print("3 - Back")
        
        elif item["type"] == "loot":
            print("1 - Drop")
            print("2 - Back")
        
        else:
            print("1 - Use")
            print("2 - Drop")
            print("3 - Back")


        action_choice = input("Select action: ")

        if item["type"] in ["weapon", "armor", "accessory"]:
            if action_choice == "1":
                equip_item(player, index, item)
            elif action_choice == "2":
                drop_item(player, index)
                index, item = select_item(player)
                if index is None:
                    return
            elif action_choice == "3":
                break
        elif item["type"] == "loot":
            if action_choice == "1":
                drop_item(player, index)
                index, item = select_item(player)
                if index is None:
                    return
            elif action_choice == "2":
                drop_item(player, index)
                index, item = select_item(player)
                if index is None:
                    return
        else:
            if action_choice == "1":
                use_item(player, index, item)
            elif action_choice == "2":
                drop_item(player, index)
                break
            elif action_choice == "3":
                break


def enemy_drop(player, enemy):
    if enemy.get("drop") is None:
        gold_roll = random.random()
        if gold_roll < 0.65:
            gold = random.randint(enemy["gold_min"], enemy["gold_max"])
            player["gold"] += gold
            print(f"You found {gold} gold!")
            return

    roll = random.random()
    if roll < 0.33:
        drop = enemy["drop"]
        if isinstance(drop, dict):
            item_id = drop.get(player["class"])
        else:
            item_id = drop
        if item_id.startswith("WEAPON_"):
            with open("data/weapons.json") as file:
                data = json.load(file)
        else:
            with open("data/items.json") as file:
                data = json.load(file)
        item = data[item_id]
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