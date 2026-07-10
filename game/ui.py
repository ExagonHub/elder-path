from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os


damage_colors = {
    "physical": "bright_white",
    "fire": "bright_red",
    "frost": "turquoise2",
    "lightning": "bright_yellow",
    "critical": "#8B0000",
    "poison": "green",
    "shadow": "dark_magenta"
}

def show_status(player, enemy=None):
    console = Console()
    panel1 = Panel(f"[bold]Name:[/bold] {player["name"]}\n[bold]Class:[/bold] {player["class"]}\nLevel: {player["level"]}\nXP: [#A0A0FF]{player["xp"]}/{player["xp_to_next_level"]}[/#A0A0FF]\nHP: [bold red]{player["hp"]}/{player["max_hp"]}[/bold red]\nMP: [bold dodger_blue2]{player["mp"]}/{player["max_mp"]}[/bold dodger_blue2]\nGold: [#FFD700]{player["gold"]}[/#FFD700]", title="Player", border_style="purple4")
    panel2 = Panel(f"[cyan]STR:[/cyan] {player["str"]}\n[cyan]DEX:[/cyan] {player["dex"]}\n[cyan]INT:[/cyan] {player["int"]}\n[cyan]VIT:[/cyan] {player["vit"]}", title="Status", border_style="purple4")

    if enemy is not None:
        hp_ratio = enemy["hp"] / enemy["max_hp"]
        if hp_ratio > 0.5:
            bar_color = "green"
        elif hp_ratio > 0.25:
            bar_color = "yellow"
        else:
            bar_color = "red"

        bar_length = 20
        filled = int(hp_ratio * bar_length)
        empty = bar_length - filled
        bar = "█" * filled + "░" * empty

        panel_enemy = Panel(f"{enemy["name"]}\nHP: [{bar_color}]{bar}[/{bar_color}] {enemy["hp"]}/{enemy["max_hp"]}", title="Enemy", border_style="purple4", width=30)
        console.print(Columns([panel1, panel2, panel_enemy]))
    else:
        console.print(Columns([panel1, panel2], equal=True))


def display_inventory(player):
    table = Table(title="Inventory", border_style="purple4", show_lines=True)
    table.add_column("Slot")
    table.add_column("Item")
    table.add_column("Quality")

    quality_colors = {
        "common": "bright_white",
        "uncommon": "green",
        "rare": "cyan",
        "epic": "purple",
        "legendary": "yellow",
        "godly": "gold1"
    }



    for index, item in enumerate(player["inventory"]):
        if item == None:
            table.add_row(str(index + 1), "-", "-")
        else:
            color = quality_colors[item["quality"]]
            quality_text = f"[{color}]{item['quality']}[/{color}]"
            table.add_row(str(index + 1), item["name"], quality_text)


    console = Console()
    console.print(table)


def display_level_up(player):
    console = Console()
    panel1 = Panel(f"[bold]Name:[/bold] {player["name"]}\n[bold]Class:[/bold] {player["class"]}\nLevel: {player["level"]}\nXP: [#A0A0FF]{player["xp"]}/{player["xp_to_next_level"]}[/#A0A0FF]\nHP: [bold red]{player["hp"]}/{player["max_hp"]}[/bold red]\nMP: [bold dodger_blue2]{player["mp"]}/{player["max_mp"]}[/bold dodger_blue2]\nGold: [#FFD700]{player["gold"]}[/#FFD700]", title="Player", border_style="purple4")
    panel2 = Panel(f"[cyan]STR:[/cyan] {player["str"]}\n[cyan]DEX:[/cyan] {player["dex"]}\n[cyan]INT:[/cyan] {player["int"]}\n[cyan]VIT:[/cyan] {player["vit"]}", title="Status", border_style="purple4")
    panel_level_up = Panel(f"Level {player["level"]} reached!\n+3 Stat Points", width=20, border_style="purple4")
    console.print(Columns([panel1, panel2, panel_level_up]))


def display_combat_menu(player):
    console = Console()
    panel_combat = Panel(f"[#DA70D6]1[/#DA70D6] - Attack\n[#DA70D6]2[/#DA70D6] - Defence\n[#DA70D6]3[/#DA70D6] - Dodge\n[#DA70D6]4[/#DA70D6] - Use Item", title="Actions", border_style="purple4")
    console.print(panel_combat, width=20)


def display_main_menu():
    console = Console()
    panel_main_menu = Panel("[italic][#A0A0FF]Every beginning has its end.[/#A0A0FF][/italic]\n\n[bright_magenta]1[/bright_magenta] - [bright_white]Play[/bright_white]\n[bright_magenta]2[/bright_magenta] - [bright_white]Settings[/bright_white]\n[bright_magenta]3[/bright_magenta] - [bright_white]Quit[/bright_white]", title="E L D E R  P A T H", border_style="purple4")
    console.print(panel_main_menu, justify="center")

    version_panel = Panel("[italic bright_white]v0.7.1[/italic bright_white]", border_style="purple4", width=10)
    console.print(version_panel, justify="left")


def display_play_menu():
    console = Console()
    panel_play_menu = Panel("[bright_magenta]1[/bright_magenta] - [bright_white]New Game[/bright_white]\n[bright_magenta]2[/bright_magenta] - [bright_white]Load Game[/bright_white]", title="Welcome to the Beginning", border_style="purple4")
    console.print(panel_play_menu, justify="center")


def display_class_menu():
    console = Console()
    panel_class_choice = Panel("[bright_magenta]1[/bright_magenta] - [bold][bright_white]Warrior[/bright_white][/bold] | [#A0A0FF]Master of physical strength[/#A0A0FF]\n[bright_magenta]2[/bright_magenta] - [bold][bright_white]Assassin[/bright_white][/bold] | [#A0A0FF]Like a shadow[/#A0A0FF]\n[bright_magenta]3[/bright_magenta] - [bold][bright_white]Mage[/bright_white][/bold] | [#A0A0FF]Wielder of Magic[/#A0A0FF]", border_style="purple4")
    console.print(panel_class_choice, width=50)


def display_attack_menu(player):
    console = Console()
    panel_warrior_attack = Panel("[bright_magenta]1[/bright_magenta] - [bold][bright_white]Normal Attack[/bright_white][/bold]\n[bright_magenta]2[/bright_magenta] - [bold][bright_white]Defensive Stance[/bright_white][/bold]\n[bright_magenta]3[/bright_magenta] - [bold][bright_white]Counter Attack[/bright_white][/bold]", border_style="purple4", width=20)
    panel_assassin_attack = Panel("[bright_magenta]1[/bright_magenta] - [bold][bright_white]Normal Attack[/bright_white][/bold]\n[bright_magenta]2[/bright_magenta] - [bold][bright_white]Rapid Attack[/bright_white][/bold]\n[bright_magenta]3[/bright_magenta] - [bold][bright_white]Piercing Attack[/bright_white][/bold]", border_style="purple4", width=20)
    panel_mage_attack = Panel("[bright_magenta]1[/bright_magenta] - [bold][bright_white]Fireball[/bright_white][/bold]\n[bright_magenta]2[/bright_magenta] - [bold][bright_white]Frost[/bright_white][/bold]\n[bright_magenta]3[/bright_magenta] - [bold][bright_white]Lightning[/bright_white][/bold]", border_style="purple4", width=20)
    if player["class"] == "Warrior":
        console.print(panel_warrior_attack)
    elif player["class"] == "Assassin":
        console.print(panel_assassin_attack)
    elif player["class"] == "Mage":
        console.print(panel_mage_attack)


def display_enemy_info(enemy):
    console = Console()
    hp_ratio = enemy["hp"] / enemy["max_hp"]
    if hp_ratio > 0.5:
        bar_color = "green"
    elif hp_ratio > 0.25:
        bar_color = "yellow"
    else:
        bar_color = "red"

    bar_length = 20
    filled = int(hp_ratio * bar_length)
    empty = bar_length - filled
    bar = "█" * filled + "░" * empty

    panel = Panel(f"{enemy["name"]}\nHP: [{bar_color}]{bar}[/{bar_color}] {enemy["hp"]}/{enemy["max_hp"]}", title="Enemy", border_style="purple4", width=30)
    console.print(panel, justify="right")


def display_equipment(player):
    console = Console()
    armor_table = Table(title="Armor", border_style="purple4")
    armor_table.add_column("Slot Name")
    armor_table.add_column("Item Name")

    helmet = player["equipment"]["helmet"]["name"] if player["equipment"]["helmet"] is not None else "[ empty ]"

    armor_table.add_row("Helmet", helmet)

    chest = player["equipment"]["chest"]["name"] if player["equipment"]["chest"] is not None else "[ empty ]"

    armor_table.add_row("Chest", chest)

    gloves = player["equipment"]["gloves"]["name"] if player["equipment"]["gloves"] is not None else "[ empty ]"

    armor_table.add_row("Gloves", gloves)

    boots = player["equipment"]["boots"]["name"] if player["equipment"]["boots"] is not None else "[ empty ]"

    armor_table.add_row("Boots", boots)

    char_table = Table(title="Character", border_style="purple4")
    char_table.add_column("")
    char_table.add_column("")

    char_table.add_row("Name", player["name"])
    char_table.add_row("Class", player["class"])
    char_table.add_row("Level", str(player["level"]))
    char_table.add_row("Accessory", player["equipment"]["accessory"]["name"] if player["equipment"]["accessory"] is not None else "[ empty ]")

    weapon_table = Table(title="Weapons", border_style="purple4")
    weapon_table.add_column("Slot Name")
    weapon_table.add_column("Item Name")

    two_hand = player["equipment"]["two_hand"]

    if two_hand is not None:
        weapon_table.add_row("Main hand", "[ locked ]")
        weapon_table.add_row("Off hand", "[ locked ]")
    else:
        main_hand = player["equipment"]["main_hand"]["name"] if player["equipment"]["main_hand"] is not None else "[ empty ]"
        weapon_table.add_row("Main hand", main_hand)

        off_hand = player["equipment"]["off_hand"]["name"] if player["equipment"]["off_hand"] is not None else "[ empty ]"
        weapon_table.add_row("Off hand", off_hand)

    two_hand_name = two_hand["name"] if two_hand is not None else "[ empty ]"
    weapon_table.add_row("Two-hand", two_hand_name)

    Columns([armor_table, char_table, weapon_table])

    console.print(Columns([armor_table, char_table, weapon_table]))


def display_game_menu():
    console = Console()
    panel = Panel("[bright_magenta]1[/bright_magenta] - [bright_white]Combat[/bright_white]\n[bright_magenta]2[/bright_magenta] - [bright_white]Equipment[/bright_white]\n[bright_magenta]3[/bright_magenta] - [bright_white]Travel[/bright_white]\n[bright_magenta]4[/bright_magenta] - [bright_white]More[/bright_white]", title="Game Menu", border_style="purple4")

    console.print(panel, justify="center")


def display_room(location):
    console = Console()
    panel = Panel(f"{location['name']} | {location['zone_type']}\nPaths: {', '.join(k.upper() for k in location['connections'].keys())}", title="Room Information", border_style="purple4")
    console.print(panel, justify="center")

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear") 


def display_more_menu(player):
    from game.world import get_location
    zone_type = get_location(player)["zone_type"]

    if zone_type == "green":
        menu_text = "[bright_magenta]1[/bright_magenta] - [bright_white]NPC's[/bright_white]\n[bright_magenta]2[/bright_magenta] - [bright_white]Quit Game[/bright_white]\n[bright_magenta]3[/bright_magenta] - [bright_white]Back[/bright_white]"
    else:
        menu_text = "[bright_magenta]1[/bright_magenta] - [bright_white]Quit Game[/bright_white]\n[bright_magenta]2[/bright_magenta] - [bright_white]Back[/bright_white]"

    console = Console()
    panel = Panel(menu_text, title="More", border_style="purple4")
    console.print(panel, justify="center")
    choice = input("Select: ")
    return choice


def display_npc_list(npcs, player):
    current_npcs = []
    for _, npc in npcs.items():
        if npc["location"] == player["current_room"]:
            current_npcs.append(npc)

    console = Console()
    menu_text = ""
    for i, npc in enumerate(current_npcs):
        menu_text += f"[bright_magenta]{i + 1}[/bright_magenta] - [bright_white]{npc['name']}[/bright_white]\n"
    menu_text += f"[bright_magenta]{len(current_npcs) + 1}[/bright_magenta] - [bright_white]Back[/bright_white]"

    panel = Panel(menu_text, title="NPC's", border_style="purple4")
    console.print(panel, justify="center")

    choice = input("Select: ")
    return choice, current_npcs


def display_equipment_menu():
    console = Console()
    panel = Panel("[bright_magenta]1[/bright_magenta] - [bright_white]Equip[/bright_white]\n[bright_magenta]2[/bright_magenta] - [bright_white]Unequip[/bright_white]\n[bright_magenta]3[/bright_magenta] - [bright_white]Back[/bright_white]", title="Equipment", border_style="purple4")

    console.print(panel, justify="center")

    choice = input("Select: ")
    return choice










if __name__ == "__main__":
    test_player = {
        "name": "Novekz",
        "class": "Assassin",
        "level": 1,
        "hp": 100,
        "max_hp":120,
        "mp": 100,
        "max_mp":100,
        "gold": 1000,
        "str": 1,
        "dex": 1,
        "int": 1,
        "vit": 1,
        "xp": 90,
        "xp_to_next_level": 90,
        "inventory": [
            {"name": "Health Potion", "quality": "Common"},
            {"name": "Wolf Fang", "quality": "Uncommon"},
            None 
        ] 
    }
    # display_level_up(test_player)
    # display_combat_menu(test_player)
    # display_main_menu()
    # display_play_menu()
    display_class_menu()

