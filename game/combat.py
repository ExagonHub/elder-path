import random
from game.character import level_up
from game.items import enemy_drop
from game.items import item_action
from game.ui import show_status
from game.ui import display_combat_menu
from game.ui import damage_colors
from rich.console import Console
from game.ui import display_attack_menu
from game.ui import display_enemy_info
from game.equipment import get_total_stats
from game.world import death_penalty
from game.ui import clear_terminal

console = Console()

attack_to_damage = {
    "normal": "physical",
    "rapid": "physical",
    "piercing": "physical",
    "defensive": "physical",
    "counter": "physical",
    "fireball": "fire",
    "frost": "frost",
    "lightning": "lightning"
}

def start_combat(player, enemy, zone_type, is_fixed=False):
    enemy["max_hp"] = enemy["hp"]


    stunned = False
    is_defending = False
    dodged = False
    phase = 1
    
    while (player["hp"] > 0) and (enemy["hp"] > 0):
        clear_terminal()
        show_status(player, enemy)


        display_combat_menu(player, is_fixed=is_fixed)

        action_choice = input("Select your action: ")

        if action_choice in ["1","2","3","4","5"]:
            if action_choice == "1":
                if player["class"] == "Warrior":
                    damage, attack_type = warrior_attack(player, enemy)
                    if attack_type == "normal":
                        enemy["hp"] -= damage
                    elif attack_type == "defensive":
                        enemy["hp"] -= damage // 2
                        is_defending = True
                    elif attack_type == "counter":
                        enemy["hp"] -= damage

                elif player["class"] == "Assassin":
                    damage, attack_type = assassin_attack(player, enemy)
                    if attack_type == "normal":
                        enemy["hp"] -= damage
                    elif attack_type == "rapid":
                        enemy["hp"] -= damage * 2
                    elif attack_type == "piercing":
                        enemy["hp"] -= damage

                elif player["class"] == "Mage":
                    damage, attack_type = mage_attack(player, enemy)
                    if attack_type == "fireball":
                        enemy["hp"] -= damage
                    elif attack_type == "frost":
                        enemy["hp"] -= damage
                        stunned = True
                    elif attack_type == "lightning":
                        enemy["hp"] -= damage

                if attack_type == "rapid":
                    color = damage_colors[attack_to_damage[attack_type]]
                    console.print(f"[{color}]You dealt {damage * 2} damage with rapid to {enemy["name"]}! (2x {damage})[/{color}]")
                else:
                    color = damage_colors[attack_to_damage[attack_type]]
                    console.print(f"[{color}]You dealt {damage} damage with {attack_type} to {enemy["name"]}![/{color}]")

                if enemy.get("phase_based"):
                    defense_chance = enemy.get("phase2", {}).get("defense_chance", 0) if phase == 2 else enemy.get("phase1_defense_chance", 0)
                    if random.random() < defense_chance:
                        enemy["hp"] += enemy["base_damage"] // 2
                        print(f"{enemy["name"]} braces and absorbs part of the blow!")

            elif action_choice == "2":
                is_defending = True
                print("You brace for the attack!")

            elif action_choice == "3":
                roll = random.random()
                if roll < player["dex"] * 0.05:
                    dodged = True
                else:
                    player["hp"] -= enemy["base_damage"]
                    print(f"You failed to dodge! {enemy["name"]} dealt {enemy["base_damage"]} to you!")

            elif action_choice == "4":
                item_action(player)

            elif action_choice == "5" and not is_fixed:
                flee_roll = random.random()
                if flee_roll < player["dex"] * 0.05:
                    print("You successfully fled!")
                    input("\nPress Enter to continue...")
                    clear_terminal()
                    player["current_room"] = player["previous_room"]
                    break
                else:
                    print("You failed to flee!")
                    player["hp"] -= enemy["base_damage"]
                    print(f"{enemy["name"]} strikes you as you turn to run! {enemy["base_damage"]} damamge!")
                    input("\nPress Enter to continue...")
                    clear_terminal()

            if enemy["hp"] > 0:
                if enemy.get("phase_based") and phase == 1 and enemy["hp"] <= enemy["max_hp"] * 0.5:
                    phase = 2
                    print(f"\n{enemy["name"]}'s wounds turn to fury. The air grows heavy.")
                    input("\nPress Enter to continue...")
                    clear_terminal()
                if phase == 2 and enemy.get("phase_based"):
                    enemy["base_damage"] = enemy.get("phase2", {}).get("base_damage", enemy["base_damage"])
                    enemy["elemental_damage"] = enemy.get("phase2", {}).get("elemental_damage", enemy["elemental_damage"])
                if zone_type != "red" and enemy.get("can_flee", True):
                    if enemy["hp"] <= enemy["max_hp"] * 0.2:
                        print(f"{enemy["name"]} is badly wounded and flees!")
                        input("\nPress Enter to continue...")
                        clear_terminal()
                        break

                
                if stunned:
                    print(f"{enemy["name"]} is stunned and cannot attack!")
                    stunned = False
                elif dodged:
                    print(f"You successfully dodged the attack!")
                    dodged = False
                elif is_defending:
                    player["hp"] -= enemy["base_damage"] // 2
                    print(f"{enemy["name"]} dealt {enemy["base_damage"] // 2} damage to you! (Blocked)")
                    is_defending = False
                else:
                    physical_damage = max(0, enemy["base_damage"] - get_total_stats(player)["defense"])

                    if enemy.get("element"):
                        elemental_damage = max(enemy["elemental_damage"] - get_total_stats(player)["magic_resistance"], 1)
                    else:
                        elemental_damage = 0

                    actual_damage = physical_damage + elemental_damage
                    player["hp"] -= actual_damage

                    player["hp"] = max(0, player["hp"])

                    if elemental_damage > 0:
                        print(f"{enemy['name']} dealt {physical_damage} physical and {elemental_damage} {enemy['element']} damage to you!")
                    else:
                        print(f"{enemy['name']} dealt {actual_damage} damage to you!")


        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4")

    if player["hp"] <= 0:
        print("You have been defeated.")
        death_penalty(player)
        input("\nA true warrior never gives up. Rise and continue your story... Press Enter to revive.")
        clear_terminal()
        return "defeat"
        

    elif enemy["hp"] <= 0 and player["hp"] > 0:
        print(f"Victory ! You defeated {enemy["name"]} !")
        player["xp"] += enemy["xp"]
        print(f"You gained {enemy["xp"]} XP !")
        enemy_drop(player, enemy)
        level_up(player)
        if is_fixed and player["current_room"] not in player.get("cleared_rooms", []):
            player.setdefault("cleared_rooms", []).append(player["current_room"])
        input("\nPress Enter to continue...")
        clear_terminal()
        return "victory"


def warrior_attack(player, enemy):
    while True:
        display_attack_menu(player)

        stance_choice = input("Select your stance: ")

        bonus = player["str"] // 2
        damage = get_total_stats(player)["base_damage"] + bonus

        if stance_choice in ["1","2","3"]:
            if stance_choice == "1":
                return damage, "normal"
            
            elif stance_choice == "2":
                return damage // 2, "defensive"
            
            elif stance_choice == "3":
                roll = random.random()
                if roll < 0.5:
                    damage = int(damage * 1.5)
                    return damage, "counter"
                else:
                    return 0, "counter"
                
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")
                

def assassin_attack(player, enemy):
    while True:
        display_attack_menu(player)

        stance_choice = input("Select your stance: ")

        bonus = player["dex"] // 2
        damage = get_total_stats(player)["base_damage"] + bonus

        if stance_choice in ["1","2","3"]:
            if stance_choice == "1":
                return damage, "normal"
            
            elif stance_choice == "2":
                return damage // 2, "rapid"
            
            elif stance_choice == "3":
                roll = random.random()
                if roll < 0.5:
                    return int(damage * 1.5), "piercing"
                else:
                    return 0, "piercing"
                
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


def mage_attack(player, enemy):
    while True:
        display_attack_menu(player)

        stance_choice = input("Select your choice: ")

        bonus = player["int"] // 2
        damage = get_total_stats(player)["base_damage"] + bonus

        if stance_choice in ["1","2","3"]:
            if stance_choice == "1":
                roll = random.random()
                if roll < 0.5:
                    return int(damage * 1.5), "fireball"
                else:
                    return damage, "fireball"
                
            elif stance_choice == "2":
                return damage, "frost"
            
            elif stance_choice == "3":
                return damage, "lightning"
            
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")