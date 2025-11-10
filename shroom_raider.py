from argparse import ArgumentParser
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# returns the converted map
def convert_map(stage_map: list) -> str:
    converted_map = []

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

    for row in stage_map:
        converted_row = []
        for char in row:
            converted_row.append(ui_representation.get(char, char))
        converted_map.append("".join(converted_row))

    return "\n".join(converted_map)

def get_player_position(stage_map: list):
    for y, row in enumerate(stage_map):
        for x, char in enumerate(row):
            if char == "L":
                return x, y

# helper function to move the player while restoring underlying tile
def move_player(stage_map, player_x, player_y, target_x, target_y, under_player):
    stage_map[player_y][player_x] = under_player
    new_under = stage_map[target_y][target_x]
    stage_map[target_y][target_x] = "L"
    return target_x, target_y, new_under

GROUND_OBJECTS = ["T", "R", "+", "*", "x"]


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("stage_file", nargs="?", default="stage_map.txt")
    args = arg_parser.parse_args()

    with open(args.stage_file, encoding="utf-8") as stage_file:
        stage_map = [list(line.rstrip("\n")) for line in stage_file.readlines()]

    player_x, player_y = get_player_position(stage_map)
    if player_x is None:
        print("No player (L) found in stage file.")
        return

    under_player = "."  # initial tile under player

    clear()
    print(convert_map(["".join(row) for row in stage_map]))

    game_state = True
    while game_state:
        user_input = input("enter input: ").lower()
        if user_input == "exit":
            break

        for move in user_input:
            target_x = player_x
            target_y = player_y

            if move == "w":
                target_y -= 1
            elif move == "s":
                target_y += 1
            elif move == "a":
                target_x -= 1
            elif move == "d":
                target_x += 1
            else:
                continue  # ignore invalid input

            if not (0 <= target_y < len(stage_map)) or not (0 <= target_x < len(stage_map[0])):
                continue  # out of bounds

            target_tile = stage_map[target_y][target_x]

            # handle rock
            if target_tile == "R":
                dx = target_x - player_x
                dy = target_y - player_y
                rock_x = target_x + dx
                rock_y = target_y + dy

                if not (0 <= rock_y < len(stage_map)) or not (0 <= rock_x < len(stage_map[0])):
                    continue  # rock push out of bounds

                rock_dest = stage_map[rock_y][rock_x]

                # cannot push rock onto tree, rock, or powerup
                if rock_dest in GROUND_OBJECTS:
                    continue

                # rock pushed into water: disappears, tile becomes '_'
                if rock_dest == "~":
                    stage_map[rock_y][rock_x] = "_"
                    # remove rock from old position
                    stage_map[target_y][target_x] = "." 
                    player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, ".")
                    continue

                # rock pushed onto floor or _: allowed
                if rock_dest in [".", "_"]:
                    # move rock to destination
                    stage_map[rock_y][rock_x] = "R"
                    # remove rock from old position
                    stage_map[target_y][target_x] = "." 
                    player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, ".")
                    continue

            # blocked by tree
            if target_tile == "T":
                continue

            # player falls in water: game over
            if target_tile == "~":
                stage_map[player_y][player_x] = under_player
                stage_map[target_y][target_x] = "L"
                player_x, player_y = target_x, target_y
                clear()
                print(convert_map(["".join(row) for row in stage_map]))
                print("You fell into the water. Game over.")
                game_state = False
                break

            # normal move: floor, _, or powerup
            if target_tile in [".", "_", "+", "*", "x"]:
                player_x, player_y, under_player = move_player(stage_map, player_x, player_y, target_x, target_y, under_player)
                continue

        clear()
        print(convert_map(["".join(row) for row in stage_map]))

main()
