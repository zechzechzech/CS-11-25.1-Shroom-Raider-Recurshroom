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

def apply_move(move, stage_map, player_x, player_y, under_player, held_item, score, total_mushrooms):
    move = move.lower()

    if move == "p":
        if under_player in PICKUP_ITEMS and PICKUP_ITEMS[under_player] != "mushroom":
            if held_item in PICKUP_ITEMS.values():
                return player_x, player_y, under_player, held_item, score
            else:
                held_item = PICKUP_ITEMS[under_player]
                under_player = "."
        return player_x, player_y, under_player, held_item, score

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
        return player_x, player_y, under_player, held_item, score

    if not (0 <= target_y < len(stage_map)) or not (0 <= target_x < len(stage_map[0])):
        return player_x, player_y, under_player, held_item, score

    target_tile = stage_map[target_y][target_x]

    if target_tile == "T":
        if held_item == "axe":
            stage_map[target_y][target_x] = "."
            held_item = None
            new_x, new_y, new_under = move_player(stage_map, player_x, player_y, target_x, target_y, under_player)
            return new_x, new_y, new_under, held_item, score
        elif held_item == "flamethrower":
            burn_trees(stage_map, target_x, target_y)
            held_item = None
            new_x, new_y, new_under = move_player(stage_map, player_x, player_y, target_x, target_y, under_player)
            return new_x, new_y, new_under, held_item, score
        else:
            return player_x, player_y, under_player, held_item, score

    if target_tile == "R":
        dx, dy = target_x - player_x, target_y - player_y
        rock_x, rock_y = target_x + dx, target_y + dy

        if not (0 <= rock_y < len(stage_map)) or not (0 <= rock_x < len(stage_map[0])):
            return player_x, player_y, under_player, held_item, score

        rock_dest = stage_map[rock_y][rock_x]
        if rock_dest in GROUND_OBJECTS:
            return player_x, player_y, under_player, held_item, score

        if rock_dest == "~":
            stage_map[rock_y][rock_x] = "_"
            stage_map[target_y][target_x] = "."
            new_x, new_y, new_under = move_player(stage_map, player_x, player_y, target_x, target_y, ".")
            return new_x, new_y, new_under, held_item, score

        if rock_dest in [".", "_"]:
            stage_map[rock_y][rock_x] = "R"
            stage_map[target_y][target_x] = "."
            new_x, new_y, new_under = move_player(stage_map, player_x, player_y, target_x, target_y, ".")
            return new_x, new_y, new_under, held_item, score

    if target_tile == "~":
        stage_map[player_y][player_x] = under_player
        stage_map[target_y][target_x] = "L"
        return player_x, player_y, under_player, held_item, score

    if target_tile in [".", "_", "+", "x", "*"]:
        new_x, new_y, new_under = move_player(stage_map, player_x, player_y, target_x, target_y, under_player)
        if new_under == "+":
            score += 1
            new_under = "."
        return new_x, new_y, new_under, held_item, score

    return player_x, player_y, under_player, held_item, score

def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--stage_file",  default="stage_map.txt")
    arg_parser.add_argument("-m", "--moves", dest="moves")
    arg_parser.add_argument("-o", "--output", dest="output_file")
    args = arg_parser.parse_args()

    with open(args.stage_file, encoding="utf-8") as f:
        stage_file_list = [list(line.rstrip("\n")) for line in f.readlines()]
        first_line = ''.join(stage_file_list[0])
        cols = int(first_line.split()[0])
        rows = int(first_line.split()[1])
        stage_map = stage_file_list[1:]

    player_x, player_y = get_player_position(stage_map)
    if player_x is None:
        print("No player (L) found in map.")
        return

    total_mushrooms = sum(row.count("+") for row in stage_map)
    score = 0
    under_player = "."
    held_item = None

    if args.moves and args.output_file:
        for move in args.moves:
            player_x, player_y, under_player, held_item, score = apply_move(
                move, stage_map, player_x, player_y, under_player, held_item, score, total_mushrooms
            )
        with open(args.output_file, "w", encoding="utf-8") as out:
            out.write("CLEAR\n" if score == total_mushrooms else "NO CLEAR\n")
            for row in stage_map:
                out.write("".join(row) + "\n")
        return

    clear()
    print(convert_map(stage_map))
    print(f"Score: {score}/{total_mushrooms} | Held item: {held_item or 'None'}")
    print('[W] Move Up')
    print('[A] Move Right')
    print('[S] Move Down')
    print('[D] Move Left')
    print('[P] Pick up item')
    print('[!] Reset')

    while True:
        user_input = input("Enter input: ").lower()
        if user_input == "exit":
            break

        for move in user_input:
            if move == "!":
                main()
                return

            player_x, player_y, under_player, held_item, score = apply_move(
                move, stage_map, player_x, player_y, under_player, held_item, score, total_mushrooms
            )

        clear()
        print(convert_map(stage_map))
        print(f"Score: {score}/{total_mushrooms} | Held item: {held_item or 'None'}")
        print('[W] Move Up')
        print('[A] Move Right')
        print('[S] Move Down')
        print('[D] Move Left')
        print('[P] Pick up item')
        print('[!] Reset')

if __name__ == "__main__":
    main()
