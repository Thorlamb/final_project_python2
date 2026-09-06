# Ping Pong: Reimagined

A modernized arcade Ping Pong game built in Python using Pygame. Features local 1v1, a scaling AI opponent, a chaotic 4-player team mode, and toggleable mystery box power-ups.

---

## Features

* **Three Game Modes:**
  * **Play vs AI:** Compete across Easy, Medium, and Hard difficulties with persistent local high score tracking (`highscore.txt`).
  * **1v1 Mode:** Classic two-player local multiplayer.
  * **4-Player Mode:** 2v2 doubles match mapped so four players can share one keyboard.
* **Toggleable Power-Ups:**
  * **Green (`+`):** Doubles paddle height for 10 seconds.
  * **Orange (`>>`):** Grants an immediate 50% ball speed boost.
  * Dynamically credits the last player who struck the ball.
* **State Machine Architecture:** Clean menu navigation and gameplay state transitions.
* **Smooth Performance:** Asynchronous timer tracking at 60 FPS using `pygame.time.get_ticks()`.

---

## Controls

### Menu Navigation
* **Up / Down Arrow:** Navigate options
* **Enter:** Select option / Toggle power-ups
* **Esc:** Return to main menu during gameplay

### Gameplay Controls

| Role | Player | Move Up | Move Down |
| :--- | :--- | :--- | :--- |
| **Team Left** | Player 1 (Outer) | `W` | `S` |
| | Player 2 (Inner - 4P only) | `R` | `F` |
| **Team Right** | Player 3 (Outer / Human B) | `Up Arrow` | `Down Arrow` |
| | Player 4 (Inner - 4P only) | `I` | `K` |

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Thorlamb/final_project_python2.git](https://github.com/Thorlamb/final_project_python2.git)
   cd final_project_python2
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate      # On Windows (Git Bash)
   # source .venv/bin/activate        # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game:**
   ```bash
   python main.py
   ```

---

## Tech Stack

* **Language:** Python 3
* **Game Engine:** Pygame
* **Storage:** Local File I/O for high scores