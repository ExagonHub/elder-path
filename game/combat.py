import random
from game.character import level_up

def start_combat(player, enemy):
    print(f"You encountered a {enemy["name"]}")

    enemy["max_hp"] = enemy["hp"]

    stunned = False
    is_defending = False
    dodged = False
    
    while (player["hp"] > 0) and (enemy["hp"] > 0):

        print("1 - Attack")
        print("2 - Defence")
        print("3 - Dodge")

        action_choice = input("Select your action: ")

        if action_choice in ["1","2","3"]:
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
                    print(f"You dealt {damage * 2} damage with rapid to {enemy["name"]}! (2x {damage})")
                else:
                    print(f"You dealt {damage} damage with {attack_type} to {enemy["name"]}!")

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

            if enemy["hp"] <= enemy["max_hp"] * 0.2:
                print(f"{enemy["name"]} is badly wounded and flees!")
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
                player["hp"] -= enemy["base_damage"]
                print(f"{enemy["name"]} dealt {enemy["base_damage"]} damage to you !")

        else:
            print("Invalid choice. Please enter 1 or 2")

    if player["hp"] <= 0:
        print("You have been defeated.")

    elif enemy["hp"] <= 0:
        print(f"Victory ! You defeated {enemy["name"]} !")
        player["xp"] += enemy["xp"]
        print(f"You gained {enemy["xp"]} XP !")
        level_up(player)


def warrior_attack(player, enemy):
    while True:
        print("1 - Normal Attack")
        print("2 - Defensive Stance")
        print("3 - Counter Attack")

        stance_choice = input("Select your stance: ")

        bonus = player["str"] // 2
        damage = player["base_damage"] + bonus

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
        print("1 - Normal Attack")
        print("2 - Rapid Attack")
        print("3 - Piercer Attack")

        stance_choice = input("Select your stance: ")

        bonus = player["dex"] // 2
        damage = player["base_damage"] + bonus

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
        print("1 - Fireball")
        print("2 - Frost")
        print("3 - Lightning")

        stance_choice = input("Select your choice: ")

        bonus = player["int"] // 2
        damage = player["base_damage"] + bonus

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