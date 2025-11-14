# Shroom Raider

**Shroom Raider** is a terminal-based adventure game where players collect mushrooms, navigate obstacles, and use special items to overcome challenges.

---

## Features

- Navigate a 2D map using **W/A/S/D** or **U/L/D/R** keys.
- Collect mushrooms to win.
- Interact with trees using **axe** or **flamethrower**.
- Push rocks to clear paths.
- Pick up special items using **P**.
- Reset the stage anytime with **!**.
- Main menu with ASCII title and options:
  - Read the Ranger's Notes (tutorial)
  - Enter the Forest (start game)
  - Run Away (exit)
- Game ends if the player falls into water or collects all mushrooms.
- Real-time score tracking and inventory display.

---

## Requirements

- Python 3.7+
- Terminal or command line interface
- Third-party dependencies:
  - `colorama`
  - `pytest` (for unit tests)

Install dependencies:
```
python3 -m pip install -r requirements.txt
```

---

## Installation

1. Clone or download the repository:
```
git clone <your-repo-url>
cd shroom-raider
```
2. Ensure you have a map file (default: `stage_map.txt`) in the project directory.

---

## How to Play

1. Run the game:
```
python shroom_raider.py
```
2. Main Menu options:
- **Read the Ranger's Notes** – Tutorial instructions and tips.  
- **Enter the Forest** – Start the game.  
- **Run Away** – Exit the game.  

3. Controls in the forest:
- **W** – Move up  
- **A** – Move left  
- **S** – Move down  
- **D** – Move right  
- **P** – Pick up item  
- **!** – Reset stage  
- **exit** – Quit the game

4. Objectives:
- Collect all mushrooms (`+`).  
- Chop trees (`T`) with axe (`x`) or burn with flamethrower (`*`).  
- Push rocks (`R`) to clear paths.  
- Avoid water (`~`) or the game ends.  

---

## Map File Format

- First line: **number of rows and columns**  
```
5 10
```
- Remaining lines: map symbols

| Symbol | Description                |
| ------ | -------------------------- |
| L      | Player start position      |
| T      | Tree                       |
| +      | Mushroom (collectible)     |
| R      | Rock (pushable)            |
| x      | Axe (pickable)             |
| *      | Flamethrower (pickable)    |
| ~      | Water (danger, game over)  |
| _      | Ground after filling water |
| .      | Empty ground               |

---

## Example Map (`stage_map.txt`)

```
5 10
..........  
..T+R..*..  
..L....T..  
..T..x....  
~~~~......  
```

---

## Bonus Features

- ASCII **Shroom Raider** title in main menu.
- Story-based tutorial (Ranger's Notes).
- Multiple movement schemes (W/A/S/D + U/L/D/R).
- Stage reset feature (! key).
- Interactive score and inventory tracking.

---

## Running Tests

Run all unit tests using pytest:
```
pytest
```

---

## Requirements File (`requirements.txt`)
```
colorama
pytest
```

