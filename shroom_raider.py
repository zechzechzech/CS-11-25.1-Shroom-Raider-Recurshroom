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
    ".": "\u3000",
    "\n": "\u3000"
    }

    # goes through every row and character then appends to the converted_row list
    for row in stage_map:
        converted_row = []
        for char in row:
            converted_row.append(ui_representation[char])

        # appends converted_row as a string to the converted_map list 
        converted_map.append("".join(converted_row))

    return "\n".join(converted_map)

def get_player_position(stage_map: list):
    for y, row in enumerate(stage_map):
        for x, char in enumerate(row):
            if char == "L":
                return x, y


# TODO: add things like push rock, pickup items and collision
# updates player position
def update_map(player_x, player_y, stage_map):
    new_map = []

    for y, row in enumerate(stage_map):
        new_row = []

        for x, char in enumerate(row):
            if x == player_x and y == player_y:
                new_row.append("L")
            elif char == "L":
                new_row.append(".")
            else:
                new_row.append(char)

        new_map.append("".join(new_row))

    return new_map
    
def interact(player_x, player_y, stage_map):
    new_map = []

    for y, row in enumerate(stage_map):
        new_row = []

        for x, char in enumerate(row):
            if x == player_x and y == player_y and char in {'x','*'} :
                new_row.append(".")
            else:
                new_row.append(char)

        new_map.append("".join(new_row))

    return new_map

def main():
    # argument in the terminal for stage file
    arg_parser = ArgumentParser()
    arg_parser.add_argument("stage_file", nargs="?", default="stage_map.txt")
    args = arg_parser.parse_args()

    # opens the txt file with the stage map
    with open(args.stage_file, encoding="utf-8") as stage_file:
        stage_map = stage_file.readlines()


    # gets the player's original position
    player_x, player_y = get_player_position(stage_map)

    held_item = None


    # clears the terminal
    clear()
    # converts ascii map to ui representation    
    print(convert_map(update_map(player_x, player_y, stage_map)))
    print(held_item)

    game_state = True
    while game_state:
        user_input = input("enter input: ").lower()

        # stop if entered exit
        if user_input == "exit":
            game_state = False
            break

        # counts the amount of w's or whatever to move
        for move in user_input:
            target_x = player_x
            target_y = player_y

            # 0, 0 starts at top left so subtracting y moves upwards and vice versa
            if move == "w":
                target_y -= 1
            
            elif move == "s":
                target_y += 1
                
            elif move == "a":
                target_x -= 1
                
            elif move == "d":
                target_x += 1

            elif move == 'p':
                stage_map = interact(player_x, player_y, stage_map)

            # if theres a tree, just dont update the map lmfao
            if stage_map[target_y][target_x] == "T":
                continue
            else:
                # updates to the actual position if the target position is free
                player_y = target_y
                player_x = target_x

        clear()
        # converts ascii map to ui representation
        print(convert_map(update_map(player_x, player_y, stage_map)))
        print(held_item)


# P.S. IM SORRY TO WHOEVER IS READING AND CHANGING THIS CODE
# NOTE: FEEL FREE TO CHANGE KAHIT SAAN SA CODE KO CUZ IK THAT IT LOOKS LIKE SHIT
# LIKE MAKE IT PRETTIER AND MORE READABLE AND WORK BETTER OR WHATEVER
# PWEDE RIN GAWA PA KAYO FUNCTIONS AND LIKE REPLACE THE CODE SA MAIN FUNCTION
# CUZ LOWKEY LINAGAY KO SA MAIN FUNCTION YUNG KARAMIHAN
# MAH BAD
main()
