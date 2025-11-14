import os
from argparse import ArgumentParser
from collections import deque

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


def handle_action(move, stage_map, px, py, under_tile, held_item, score, total_mmushrooms):
    if move == "p":
        new_held, new_under, msg = pick_item(under_tile, held_item)
        if new_under is not None:
            under_tile = new_under
        return px, py, under_tile, new_held, score, False, msg

    tx, ty = px, py
    if move == "w":
        ty -= 1
    elif move == "s":
        ty += 1
    elif move == "a":
        tx -= 1
    elif move == "d":
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


def main():
    parser = ArgumentParser()
    parser.add_argument("stage_file", nargs="?", default="stage_map.txt")
    stage_file = parser.parse_args().stage_file

    try:
        stage_map = load_stage_map(stage_file)
    except FileNotFoundError:
        print(f"Error: Stage file '{stage_file}' not found.")
        return
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    px, py = get_player_position(stage_map)
    if px is None:
        print("Error: Player 'L' not found on map.")
        return

    under_tile = "."
    held_item = None
    total_mushrooms = sum(row.count("+") for row in stage_map)
    score = 0
    message = ""

    while True:
        clear()
        print(convert_map(stage_map))
        print(f"Score: {score}/{total_mushrooms} | Held: {held_item or 'None'}")

        if message:
            print(f"\n{message}")

        user_input = input("\nEnter input (w,a,s,d,p) or 'exit': ").lower()
        if user_input == "exit":
            break

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