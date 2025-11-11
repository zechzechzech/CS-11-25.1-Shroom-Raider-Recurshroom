import pytest
from shroom_raider import (
    convert_map,
    get_player_position,
    move_player,
    burn_trees,
)

# --- convert_map -------------------------------------------------------------
def test_convert_map_symbols():
    raw = [["L", "T", "+", "R", "x", "*", "~", "_", ".", "\n"]]
    out = convert_map(raw)

    assert "🧑" in out
    assert "🌲" in out
    assert "🍄" in out
    assert "🪨" in out
    assert "🪓" in out
    assert "🔥" in out
    assert "🟦" in out
    assert "⬜" in out

# --- get_player_position -----------------------------------------------------
def test_get_player_position_found():
    stage = [list("..."), list(".L."), list("...")]
    x, y = get_player_position(stage)
    assert (x, y) == (1, 1)

def test_get_player_position_not_found():
    stage = [list("..."), list("...")]
    x, y = get_player_position(stage)
    assert (x, y) == (None, None)

# --- move_player -------------------------------------------------------------
def test_move_player_swaps_correctly():
    stage = [list("L."), list("..")]
    px, py = 0, 0
    tx, ty = 1, 0
    px, py, under = move_player(stage, px, py, tx, ty, ".")
    assert (px, py) == (1, 0)
    assert under == "."
    assert stage[0][0] == "."
    assert stage[0][1] == "L"

# --- burn_trees --------------------------------------------------------------
def test_burn_trees_connected_group():
    stage = [
        list("TTT"),
        list("TTT"),
        list("TT.")
    ]
    burn_trees(stage, 1, 1)

    assert all(ch == "." for row in stage for ch in row if ch != ".")

def test_burn_trees_does_not_burn_isolated():
    stage = [
        list("T.T"),
        list(".T."),
        list("T.T")
    ]
    burn_trees(stage, 1, 1)

    assert stage[1][1] == "."
    assert stage[0][0] == "T"
    assert stage[2][2] == "T"

def test_player_can_move_to_empty_tile():
    stage = [list("L."), list("..")]
    px, py = 0, 0
    tx, ty = 1, 0
    px, py, under = move_player(stage, px, py, tx, ty, ".")
    assert stage[0][1] == "L"
    assert stage[0][0] == "."

