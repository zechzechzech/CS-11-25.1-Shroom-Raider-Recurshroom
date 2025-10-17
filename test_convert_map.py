# for unit testing of test_sample.py
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

def test_convert_map():
    # opens the txt file with the stage map
    with open("stage_map.txt") as stage_map:
        stage_map_list = stage_map.readlines()

    result = "\n".join(convert_map(stage_map_list))

    assert isinstance(result, str)
    assert "🧑" in result
    assert "🍄" in result
    assert "🌲" in result
    assert "🟦" in result
    assert "🪓" in result
    assert "🪨" in result
    assert "🔥" in result
    assert result == """\
🌲🌲🌲🌲🌲🌲🌲🌲🌲  
🌲      🍄      🌲  
🌲      🟦      🌲  
🌲      🪨  🌲  🌲  
🌲  🌲  🧑🌲🌲  🌲  
🌲  🪓      🔥  🌲  
🌲              🌲  
🌲              🌲  
🌲🌲🌲🌲🌲🌲🌲🌲🌲
""".strip()


