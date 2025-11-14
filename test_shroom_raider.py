import pytest
from shroom_raider import (
    load_stage_map,
    get_player_position,
    interact_tree,
    handle_action,
    pick_item,
)


def test_load_stage_map(tmp_path):
    f = tmp_path / "map.txt"
    f.write_text("3 3\nTTT\nT.L\nT+T\n")
    stage = load_stage_map(str(f))
    assert len(stage) == 3
    assert len(stage[0]) == 3
    assert stage[1][2] == "L"


def test_get_player_position():
    stage = [['T', 'T', 'T'], ['T', '.', 'L'], ['T', '+', 'T']]
    x, y = get_player_position(stage)
    assert (x, y) == (2, 1)


def test_interact_tree_axe():
    stage = [['T', 'T', 'T'], ['T', 'x', 'T'], ['T', 'L', 'T']]
    px, py, under = 1, 2, "."
    held = "axe"
    
    # Test calls interact_tree directly, which returns the new player state
    new_state, held, msg = interact_tree(stage, 'T', 1, 1, held, px, py, under)
    px, py, new_under = new_state
    
    # Assert player is now at (1, 1)
    assert stage[1][1] == "L" 
    # Assert player's old spot (1, 2) is now '.'
    assert stage[2][1] == "."
    # Assert the returned 'under' tile (what the player is on) is '.'
    assert new_under == "."
    assert held is None
    assert (px, py) == (1, 1)


def test_interact_tree_flamethrower():
    stage = [['T', 'T', 'T'], ['T', 'T', 'T'], ['T', 'L', 'T']]
    px, py, under = 1, 2, "."
    held = "flamethrower"
    new_state, held, msg = interact_tree(stage, 'T', 1, 1, held, px, py, under)
    px, py, new_under = new_state
    
    # Check that all trees are gone (except where the player moved to)
    for r_idx, row in enumerate(stage):
        for c_idx, cell in enumerate(row):
            if (c_idx, r_idx) == (px, py):
                assert cell == 'L' # Player is here
            else:
                assert cell != 'T' # No other trees
    assert held is None


def test_push_rock_floor():
    # Map MUST be 4 rows to have space to push the rock
    stage = [['.', '.', '.'], ['.', 'L', '.'], ['.', 'R', '.'], ['.', '.', '.']]
    px, py, under = 1, 1, "."
    
    # New handle_action returns 7 values
    px, py, under, held, score, ended, msg = handle_action("s", stage, px, py, under, None, 0, 0)
    
    assert stage[2][1] == "L" # Player moved to (1, 2)
    assert stage[1][1] == "." # Old spot is now '.'
    assert stage[3][1] == "R" # Rock is at (1, 3)
    assert not ended


def test_push_rock_water():
    # Map MUST be 4 rows and have water in the right spot
    stage = [['.', '.', '.'], ['.', 'L', '.'], ['.', 'R', '.'], ['.', '~', '.']]
    px, py, under = 1, 1, "."
    px, py, under, held, score, ended, msg = handle_action("s", stage, px, py, under, None, 0, 0)
    
    assert stage[3][1] == "_" # Water at (1, 3) becomes bridge
    assert stage[2][1] == "L" # Player moved to (1, 2)
    assert stage[1][1] == "." # Old spot is now '.'
    assert not ended # Pushing rock into water does NOT end the game


def test_pickup_item():
    under_tile = "x"
    held_item = None
    new_held, new_under, msg = pick_item(under_tile, held_item)
    assert new_held == "axe"
    assert new_under == "."
    assert "Picked up" in msg


def test_pickup_already_holding():
    under_tile = "*"
    held_item = "axe"
    new_held, new_under, msg = pick_item(under_tile, held_item)
    assert new_held == "axe"
    assert new_under is None
    assert "Already holding" in msg


def test_mushroom_collection():
    stage = [['.', '.', '.'], ['.', 'L', '.'], ['.', '+', '.']]
    px, py, under = 1, 1, "."
    score = 0
    total = 2  # <--- CHANGE THIS
    
    # This test no longer causes an OSError because input() is gone
    px, py, under, held, score, ended, msg = handle_action("s", stage, px, py, under, None, score, total)
    
    assert score == 1
    assert stage[2][1] == "L"
    assert under == "." # The tile the player moved *off* of
    assert "Mushroom collected" in msg  # <-- This will now pass
    
    # Collecting 1 of 2 mushrooms should NOT end the game
    assert not ended  # <--- AND CHANGE THIS


def test_win_game():
    stage = [['+', 'L']]
    px, py, under = 1, 0, "."
    score = 0
    total = 1
    
    # This test no longer causes an OSError
    px, py, under, held, score, ended, msg = handle_action("a", stage, px, py, under, None, score, total)
    assert score == 1
    assert ended
    assert "All mushrooms collected" in msg


def test_water_lose():
    stage = [['L', '~']]
    px, py, under = 0, 0, "."
    
    # This test no longer causes an OSError
    px, py, under, held, score, ended, msg = handle_action("d", stage, px, py, under, None, 0, 0)
    assert ended
    assert stage[0][1] == "L" # Player is on the water tile
    assert "fell into the water" in msg