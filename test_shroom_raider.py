from main import convert_map, main
import pytest

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


