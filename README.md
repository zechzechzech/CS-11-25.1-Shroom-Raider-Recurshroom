# Shroom Raider

**Shroom Raider** is a simple terminal-based adventure game where the player collects mushrooms, navigates obstacles like trees, rocks, and water, and can use special items like axes and flamethrowers to overcome challenges. The game is inspired by classic tile-based adventure games.

---

## Features

* Navigate a 2D map using **W/A/S/D** controls.
* Collect mushrooms to win the game.
* Interact with trees using **axe** or **flamethrower**.
* Push rocks to clear paths.
* Pick up special items like **axe** and **flamethrower** using **P**.
* Game ends if the player falls into water or collects all mushrooms.
* Real-time score tracking and inventory display.
* Main menu with introduction and ASCII art of Shroom Raider.

---

## Requirements

* Python 3.7+
* Terminal or command line interface

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

2. Main Menu:

When you start the game, you will see the following introduction:

```
███████╗██╗  ██╗██████╗  ██████╗  ██████╗ ███╗   ███╗    ██████╗  █████╗ ██╗██████╗ ███████╗██████╗ 
██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║    ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
███████╗███████║██████╔╝██║   ██║██║   ██║██╔████╔██║    ██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
╚════██║██╔══██║██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║    ██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
███████║██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║    ██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

Hi Laro Craft! Welcome to Shroom Raider.
We’re amazed by your skills in mushroom gathering.
Collect all the mushrooms hidden in the forest — can you master the game?

[1] Enter the Forest
[2] Run Away
```

* Input **1** to start the game.
* Input **2** to exit the game.

3. In-game Controls:

* **W** – Move up
* **A** – Move left
* **S** – Move down
* **D** – Move right
* **P** – Pick up item
* **exit** – Quit the game

4. Game objective:

* Collect all mushrooms (`+`) on the map.
* Use **axe** (`x`) to chop down trees (`T`).
* Use **flamethrower** (`*`) to burn clusters of trees.
* Push rocks (`R`) to clear paths.
* Avoid falling into water (`~`) or the game ends.

---

## Map File Format

* The first line of the file specifies the **number of rows and columns**:

```
5 10
```

* The remaining lines represent the map, using these symbols:

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
