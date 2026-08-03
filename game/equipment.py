def get_total_stats(player):
    total = {
        "hp": player["hp"],
        "mp": player["mp"],
        "base_damage": player["base_damage"],
        "defense": player["defense"],
        "magic_resistance": player["magic_resistance"]
    }

    for _, item in player["equipment"].items():
        if item is not None:
            if "defense" in item:
                total["defense"] += item["defense"]
            if "magic_resistance" in item:
                total["magic_resistance"] += item["magic_resistance"]
            if "damage" in item:
                total["base_damage"] += item["damage"]

    return total  


def equip_item(player, index, item):
    slot = item["slot"]

    if player["class"] not in item["allowed_classes"]:
        print(f"Your class cannot equip this item.")

        return

    if slot == "two_hand":
        if player["equipment"]["off_hand"] is not None:
            for i, inv_item in enumerate(player["inventory"]):
                if inv_item is None:
                    player["inventory"][i] = player["equipment"]["off_hand"]
                    break
            player["equipment"]["off_hand"] = None

    if player["equipment"][slot] is not None:
        for i, inv_item in enumerate(player["inventory"]):
            if inv_item is None:
                player["inventory"][i] = player["equipment"][slot]
                break
        player["equipment"][slot] = None

    player["equipment"][slot] = item

    player["inventory"][index] = None

    print(f"{item["name"]} equipped.")


def unequip_item(player, slot):
    item = player["equipment"][slot]

    if item is not None:
        if None not in player["inventory"]:
            print("Inventory is full.")
        else:
            for i, inv_slot in enumerate(player["inventory"]):
                if inv_slot is None:
                    player["inventory"][i] = item
                    break

            player["equipment"][slot] = None
            print(f"{item["name"]} unequipped.")
