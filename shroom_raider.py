from argparse import ArgumentParser
import os
from collections import deque

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def convert_map(stage_map: list) -> str:
    ui_representation = {
        "L": "🧑",
        "T": "🌲",
        "+": "🍄",
        "R": "🪨",
        "x": "🪓",
        "*": "🔥",
        "~": "🟦",
        "_": "⬜",
        ".": "\u3000",
        "\n": "\u3000"
    }
    return "\n".join(
        "".join(ui_representation.get(ch, ch) for ch in row)
        for row in stage_map
    )

def get_player_position(stage_map: list):
    for y, row in enumerate(stage_map):
        for x, ch in enumerate(row):
            if ch == "L":
                return x, y
    return None, None

def move_player(stage_map, player_x, player_y, target_x, target_y, under_player):
    stage_map[player_y][player_x] = under_player
    new_under = stage_map[target_y][target_x]
    stage_map[target_y][target_x] = "L"
    return target_x, target_y, new_under

GROUND_OBJECTS = ["T", "R", "+", "*", "x"]
PICKUP_ITEMS = {"+": "mushroom", "x": "axe", "*": "flamethrower"}

def burn_trees(stage_map, start_x, start_y):
    """Burn all connected trees (up/down/left/right)."""
    height = len(stage_map)
    width = len(stage_map[0])
    visited = set()
    queue = deque([(start_x, start_y)])
    
    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if stage_map[y][x] == "T":
            stage_map[y][x] = "."
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and stage_map[ny][nx] == "T":
                    queue.append((nx, ny))

def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("stage_file", nargs="?", default="stage_map.txt")
    args = arg_parser.parse_args()

    with open(args.stage_file, encoding="utf-8") as f:
        stage_map = [list(line.rstrip("\n")) for line in f.readlines()]

    player_x, player_y = get_player_position(stage_map)
    if player_x is None:
        print("No player (L) found in map.")
        return

    # Count total mushrooms for win condition
    total_mushrooms = sum(row.count("+") for row in stage_map)
    score = 0

    under_player = "."
    held_item = None  # axe or flamethrower

    clear()
    print(convert_map(stage_map))
    print(f"Score: {score}/{total_mushrooms} | Held item: {held_item or 'None'}")

    while True:
        user_input = input("Enter input: ").lower()
        if user_input == "exit":
            break

        # Pickup with 'P'
        if user_input == "p":
            if under_player in PICKUP_ITEMS and PICKUP_ITEMS[under_player] != "mushroom":
                held_item = PICKUP_ITEMS[under_player]
                print(f"You picked up a {held_item}!")
                under_player = "."
            else:
                print("Nothing to pick up here.")
            continue

        for move in user_input:
            # --- Pickup mid-sequence ---
            if move == "p":
                if under_player in PICKUP_ITEMS and PICKUP_ITEMS[under_player] != "mushroom":
                    held_item = PICKUP_ITEMS[under_player]
                    print(f"You picked up a {held_item}!")
                    under_player = "."
                else:
                    print("Nothing to pick up here.")
                continue

            target_x, target_y = player_x, player_y

            if move == "w":
                target_y -= 1
            elif move == "s":
                target_y += 1
            elif move == "a":
                target_x -= 1
            elif move == "d":
                target_x += 1
            else:
                continue

            if not (0 <= target_y < len(stage_map)) or not (0 <= target_x < len(stage_map[0])):
                continue

            target_tile = stage_map[target_y][target_x]


            # --- Tree interaction ---
            if target_tile == "T":
                if held_item == "axe":
                    stage_map[target_y][target_x] = "."
                    held_item = None  # consumed
                    player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, under_player)
                    continue
                elif held_item == "flamethrower":
                    burn_trees(stage_map, target_x, target_y)
                    held_item = None  # consumed
                    player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, under_player)
                    continue
                else:
                    continue

            # --- Rock pushing ---
            if target_tile == "R":
                dx, dy = target_x - player_x, target_y - player_y
                rock_x, rock_y = target_x + dx, target_y + dy

                if not (0 <= rock_y < len(stage_map)) or not (0 <= rock_x < len(stage_map[0])):
                    continue

                rock_dest = stage_map[rock_y][rock_x]
                if rock_dest in GROUND_OBJECTS:
                    continue

                if rock_dest == "~":
                    stage_map[rock_y][rock_x] = "_"
                    stage_map[target_y][target_x] = "."
                    player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, ".")
                    continue

                if rock_dest in [".", "_"]:
                    stage_map[rock_y][rock_x] = "R"
                    stage_map[target_y][target_x] = "."
                    player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, ".")
                    continue

            # --- Water = game over ---
            if target_tile == "~":
                stage_map[player_y][player_x] = under_player
                stage_map[target_y][target_x] = "L"
                clear()
                print(convert_map(stage_map))
                print("You fell into the water. Game over.")
                return

            # --- Normal movement (floor, _, or pickup) ---
            if target_tile in [".", "_", "+", "x", "*"]:
                player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, under_player)

                # After moving, check if stepped on a pickup
                if under_player == "+":
                    score += 1
                    print(f"Collected a mushroom! Score: {score}/{total_mushrooms}")
                    under_player = "."
                    if score == total_mushrooms:
                        clear()
                        print(convert_map(stage_map))
                        print("You collected all mushrooms! You win! 🎉")
                        return

                elif under_player in ["x", "*"]:
                    print(f"You stepped on a {PICKUP_ITEMS[under_player]}! Press 'P' to pick it up.")

                continue

        clear()
        print(convert_map(stage_map))
        print(f"Score: {score}/{total_mushrooms} | Held item: {held_item or 'None'}")

if __name__ == "__main__":
    main()
