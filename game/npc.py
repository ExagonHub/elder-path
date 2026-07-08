import json
from rich.columns import Columns
from rich.table import Table
from rich.console import Console
from game.ui import clear_terminal

def talk_to_npc(player, npc):
    if npc["job"] in ["weapon_seller", "armor_seller", "potion_seller"]:
        shop(player, npc)
    elif npc["job"] == "inn":
        rest(player, npc)


def shop(player, npc):
    console = Console()
    console.print(f"\n{npc['name']}: {npc['dialogue']}")

    if npc["job"] == "weapon_seller":
        buy_label = "Buy Weapon"
    elif npc["job"] == "armor_seller":
        buy_label = "Buy Armor"
    elif npc["job"] == "potion_seller":
        buy_label = "Buy Potion"


    if npc["job"] == "weapon_seller":
        stock_file = "data/weapons.json"
    elif npc["job"] == "armor_seller":
        stock_file = "data/armors.json"
    elif npc["job"] == "potion_seller":
        stock_file = "data/items.json"

    purchased = False

    while True:
        print(f"1 - {buy_label}")
        print("2 - Leave")

        choice = input("What do yu want: ")

        if choice == "1":
            with open(stock_file) as file:
                stock_data = json.load(file)
                for i, item_id in enumerate(npc["stock"]):
                    item = stock_data[item_id]
                    print(f"{i + 1} - {item['name']} ({item['quality']}) - {item['price']} gold")

                choose = input("Select item: ")
                selected_id = npc["stock"][int(choose) - 1]
                selected_item = stock_data[selected_id]

                if player["gold"] >= selected_item["price"]:
                    player["gold"] -= selected_item["price"]
                    for i, slot in enumerate(player["inventory"]):
                        if slot is None:
                            player["inventory"][i] = selected_item
                            print(f"You purchased {selected_item['name']}")
                            purchased = True
                            input("\nPress Enter to continue...")
                            clear_terminal()
                            break
                else:
                    print(f"{npc['name']}: I'm sorry friend, you don't have enough gold. How about looking at something else ?")
            if purchased:
                break
        elif choice == "2":
            print(f"\n{npc['name']}: 'Safe travels, traveler. The road ahead is dark - but so is the one behind.'")
            input("\nPress Enter to continue...")
            clear_terminal()
            break


def rest(player, npc):
    console = Console()
    console.print(f"\n{npc['name']}: {npc['dialogue']}")

    while True:
        print(f"1 - Rest({npc['price']})")
        print("2 - Leave")

        choice = input("What do you want: ")

        if choice == "1":
            if player["hp"] == player["max_hp"] and player["mp"] == player["max_mp"]:
                print(f"\n{npc['name']}: 'You already look well-rested. Come back after you've broken a sweat.'")
            else:
                if player["gold"] < npc["price"]:
                    print("I'm sorry friend, I need to make a living.")
                else:
                    player["gold"] -= npc["price"]
                    player["hp"] = player["max_hp"]
                    player["mp"] = player["max_mp"]
                    print("You rest well. Now go back to survive.")
                    input("\nPress Enter to continue...")
                    clear_terminal()
                    break

        elif choice == "2":
            print(f"{npc['name']}: 'The path of the warrior is walked alone. Go well, traveler.'")
            input("\nPress Enter to continue...")
            clear_terminal()
            break