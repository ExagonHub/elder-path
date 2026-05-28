from game.character import level_up

def start_combat(player, enemy):
    print(f"You encountered a {enemy["name"]}")
    
    while (player["hp"] > 0) and (enemy["hp"] > 0):

        print("1 - Attack")
        print("2 - Defence")

        action_choice = input("Select your action: ")

        if action_choice in ["1","2"]:
            if action_choice == "1":
                if player["class"] == "Warrior":
                    bonus = player["str"] // 2
                    damage = player["base_damage"] + bonus

                elif player["class"] == "Assassin":
                    bonus = player["dex"] // 2
                    damage = player["base_damage"] + bonus

                elif player["class"] == "Mage":
                    bonus = player["int"] // 2
                    damage = player["base_damage"] + bonus

                enemy["hp"] -= damage
                print(f"You dealt {damage} to {enemy["name"]}!")

            elif action_choice == "2":
                pass
            
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