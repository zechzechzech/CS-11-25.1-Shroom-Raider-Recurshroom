from argparse import ArgumentParser


# returns the converted map as a LIST
def convert_map(stage_map_rows: list) -> list:
    converted_map = []

    # goes through every row and character then appends to the converted_row list
    for row in stage_map_rows:
        converted_row = []
        for char in row:
            if char == "L":
                converted_row.append("🧑")
            elif char == "T":
                converted_row.append("🌲")
            elif char == "+":
                converted_row.append("🍄")
            elif char == "R":
                converted_row.append("🪨")
            elif char == "x":
                converted_row.append("🪓")
            elif char == "*":
                converted_row.append("🔥")
            elif char == "~":
                converted_row.append("🟦")
            else:
                converted_row.append("  ")

        # appends converted_row as a string to the converted_map list 
        converted_map.append("".join(converted_row))

    # returns as a list btw
    return converted_map


def main():
    # argument in the terminal for stage file
    arg_parser = ArgumentParser()
    arg_parser.add_argument("stage_file", nargs="?", default="stage_map.txt")
    args = arg_parser.parse_args()

    # opens the txt file with the stage map
    with open(args.stage_file, encoding="utf-8") as stage_map:
        stage_map_list = stage_map.readlines()

        print("\n".join(convert_map(stage_map_list)))


main()