import os
from argparse import ArgumentParser
from collections import deque
from copy import deepcopy
from colorama import init, Fore, Style

init(autoreset=True)

GROUND_OBJECTS = ["T", "R", "+", "*", "x"]
PICKUP_ITEMS = {"+": "mushroom", "x": "axe", "*": "flamethrower"}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_stage_map(filename: str):
    """Load map from file where first line contains rows and columns."""
    with open(filename, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    rows, cols = map(int, lines[0].split())
    stage_map = [list(line) for line in lines[1:1 + rows]]
    for r in stage_map:
        if len(r) != cols:
            raise ValueError("Map width mismatch")
    return stage_map


def convert_map(stage_map):
    ui = {
        "L": "🧑", "T": "🌲", "+": "🍄", "R": "🪨",
        "x": "🪓", "*": "🔥", "~": "🟦", "_": "⬜", ".": "　"
    }
    return "\n".join("".join(ui.get(ch, ch) for ch in row) for row in stage_map)


def get_player_position(stage_map):
    for y, row in enumerate(stage_map):
        for x, ch in enumerate(row):
            if ch == "L":
                return x, y
    return None, None


def move_player(stage_map, px, py, tx, ty, under_tile):
    stage_map[py][px] = under_tile
    new_under = stage_map[ty][tx]
    stage_map[ty][tx] = "L"
    return tx, ty, new_under


def burn_trees(stage_map, sx, sy):
    h, w = len(stage_map), len(stage_map[0])
    visited = set()
    queue = deque([(sx, sy)])
    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if stage_map[y][x] == "T":
            stage_map[y][x] = "."
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and stage_map[ny][nx] == "T":
                    queue.append((nx, ny))


def interact_tree(stage_map, tile, tx, ty, held_item, px, py, under_tile):
    if tile != "T":
        return None, held_item, None
    if held_item == "axe":
        stage_map[ty][tx] = "."
        return move_player(stage_map, px, py, tx, ty, under_tile), None, "Chopped down the tree."
    if held_item == "flamethrower":
        burn_trees(stage_map, tx, ty)
        return move_player(stage_map, px, py, tx, ty, under_tile), None, "Burned the trees."
    return None, held_item, "You need an axe or flamethrower to get past the tree."


def push_rock(stage_map, tx, ty, px, py):
    dx, dy = tx - px, ty - py
    rx, ry = tx + dx, ty + dy
    if not (0 <= rx < len(stage_map[0]) and 0 <= ry < len(stage_map)):
        return None
    dest = stage_map[ry][rx]
    if dest in GROUND_OBJECTS:
        return None
    if dest == "~":
        stage_map[ry][rx] = "_"
        stage_map[ty][tx] = "."
        return "."
    if dest in [".", "_"]:
        stage_map[ry][rx] = "R"
        stage_map[ty][tx] = "."
        return "."
    return None


def pick_item(under_tile, held_item):
    if held_item is not None:
        return held_item, None, "Already holding an item"
    if under_tile in PICKUP_ITEMS and PICKUP_ITEMS[under_tile] != "mushroom":
        item_name = PICKUP_ITEMS[under_tile]
        return item_name, ".", f"Picked up {item_name}"
    return held_item, None, "Nothing to pick up"


def handle_action(move, stage_map, px, py, under_tile, held_item, score, total_mushrooms):
    if move == "p":
        new_held, new_under, msg = pick_item(under_tile, held_item)
        if new_under is not None:
            under_tile = new_under
        return px, py, under_tile, new_held, score, False, msg

    tx, ty = px, py
    if move in ["w"]:
        ty -= 1
    elif move in ["s"]:
        ty += 1
    elif move in ["a"]:
        tx -= 1
    elif move in ["d"]:
        tx += 1
    else:
        return px, py, under_tile, held_item, score, False, None

    if not (0 <= tx < len(stage_map[0]) and 0 <= ty < len(stage_map)):
        return px, py, under_tile, held_item, score, False, "You can't move there."

    tile = stage_map[ty][tx]
    tree_result, held_item, msg = interact_tree(stage_map, tile, tx, ty, held_item, px, py, under_tile)
    if tree_result:
        px, py, under_tile = tree_result
        return px, py, under_tile, held_item, score, False, msg

    if tile == "R":
        res = push_rock(stage_map, tx, ty, px, py)
        if res is not None:
            px, py, under_tile = move_player(stage_map, px, py, tx, ty, res)
            return px, py, under_tile, held_item, score, False, "You pushed the rock."
        else:
            return px, py, under_tile, held_item, score, False, "The rock won't budge."

    if tile == "~":
        stage_map[py][px] = under_tile
        stage_map[ty][tx] = "L"
        return px, py, under_tile, held_item, score, True, "You fell into the water. Game over."

    if tile in [".", "_", "+", "x", "*"]:
        px, py, under_tile = move_player(stage_map, px, py, tx, ty, under_tile)
        msg = None
        if under_tile == "+":
            score += 1
            msg = f"Mushroom collected ({score}/{total_mushrooms})"
            under_tile = "."
            if score == total_mushrooms:
                return px, py, under_tile, held_item, score, True, "All mushrooms collected! You win!"
        if under_tile in ["x", "*"]:
            msg = f"Stepped on {PICKUP_ITEMS[under_tile]}. Press P to pick up."
        return px, py, under_tile, held_item, score, False, msg

    return px, py, under_tile, held_item, score, False, "You can't walk there."


# Main Menu and Tutorial
def display_tutorial():
    clear()
    print(Fore.GREEN + "Ranger's Notes:")
    print("\nWelcome, adventurer! Here are some tips to survive the forest:")
    print("- Move using W/A/S/D keys.")
    print("- Pick up special items using P.")
    print("- Reset the stage using !")
    print("- Chop trees with an axe or burn with flamethrower.")
    print("- Push rocks to clear your path.")
    print("- Collect all mushrooms to win the game.")
    print("- Avoid water or you will lose.\n")
    input("Press Enter to return to the main menu...")


def display_menu():
    clear()
    print(Fore.CYAN + """
███████╗██╗  ██╗██████╗  ██████╗  ██████╗ ███╗   ███╗    ██████╗  █████╗ ██╗██████╗ ███████╗██████╗
██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║    ██╔══██╗██╔══██║██║██╔══██╗██╔════╝██╔══██╗
███████╗███████║██████╔╝██║   ██║██║   ██║██╔████╔██║    ██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
╚════██║██╔══██║██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║    ██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
███████║██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║    ██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
""")
    print("Hi Laro Craft! Welcome to Shroom Raider.\n")
    print("We’re amazed by your skills in mushroom gathering. Collect all the mushrooms hidden in the forest — can you master the game?\n")
    print("[1] Read the Ranger's Notes")
    print("[2] Enter the Forest")
    print("[3] Run Away\n")
    choice = input("Which path will you take? (1, 2, or 3): ").strip()

    if choice == "3":
        clear()
        print("You ran away... Maybe next time!")
        exit()
    elif choice == "1":
        display_tutorial()
        return display_menu()
    elif choice == "2":
        return enter_forest_menu()
    else:
        return display_menu()


def enter_forest_menu():
    clear()
    print("You are about to enter the forest.\n")
    print("[1] Proceed into the Forest")
    print("[2] Return to Main Menu\n")
    choice = input("Which path will you take? (1 or 2): ").strip()
    if choice == "1":
        return True
    elif choice == "2":
        return False
    else:
        return enter_forest_menu()


# Main Game Loop
def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--stage_file", default="stage_map.txt", help="Stage file to load")
    parser.add_argument("-m", "--moves", default="", help="String of moves to simulate")
    parser.add_argument("-o", "--output", default="", help="Output file for simulated moves")
    args = parser.parse_args()

    try:
        original_stage_map = load_stage_map(args.stage_file)
    except FileNotFoundError:
        print(f"Error: Stage file '{args.stage_file}' not found.")
        return
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    if args.moves:  # Simulate moves and output to file
        stage_map = deepcopy(original_stage_map)
        px, py = get_player_position(stage_map)
        under_tile = "."
        held_item = None
        score = 0
        total_mushrooms = sum(row.count("+") for row in stage_map)
        for move in args.moves:
            px, py, under_tile, held_item, score, ended, _ = handle_action(
                move, stage_map, px, py, under_tile, held_item, score, total_mushrooms
            )
            if ended:
                break
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("CLEAR\n" if score == total_mushrooms else "NO CLEAR\n")
            f.write(f"{len(stage_map)} {len(stage_map[0])}\n")
            for row in stage_map:
                f.write("".join(row) + "\n")
        return

    start_game = display_menu()
    if not start_game:
        start_game = display_menu()

    stage_map = deepcopy(original_stage_map)
    px, py = get_player_position(stage_map)
    under_tile = "."
    held_item = None
    score = 0
    total_mushrooms = sum(row.count("+") for row in stage_map)
    message = ""

    while True:
        clear()
        print(convert_map(stage_map))
        print(f"Score: {score}/{total_mushrooms} | Held: {held_item or 'None'}")
        if message:
            print(f"\n{message}")

        user_input = input("\nEnter input (W/A/S/D, P to pick, ! to reset, exit to quit): ").lower()
        if user_input == "exit":
            break
        if "!" in user_input:
            stage_map = deepcopy(original_stage_map)
            px, py = get_player_position(stage_map)
            under_tile = "."
            held_item = None
            score = 0
            message = "Stage has been reset!"
            continue

        message = ""
        for act in user_input:
            px, py, under_tile, held_item, score, ended, new_message = handle_action(
                act, stage_map, px, py, under_tile, held_item, score, total_mushrooms
            )
            if new_message:
                message = new_message
            if ended:
                clear()
                print(convert_map(stage_map))
                print(f"Score: {score}/{total_mushrooms} | Held: {held_item or 'None'}")
                print(f"\n{message}")
                input("\nPress Enter to exit...")
                return


if __name__ == "__main__":
    main()
