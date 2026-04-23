# 🐝 Buzzled Master Solver

A lightweight, interactive, browser-based solver for the "Master" mode of the daily hex logic puzzle game [Buzzled](https://puzzmallow.com/buzzled) by Puzzmallow.

In Master mode, the game removes the mathematical sums and instead asks you to match the exact count of colored hexes for each row across three different directional axes. This solver uses a **constraint propagation and backtracking algorithm** to instantly find the correct grid layout based on the daily pins.

---

## ✨ Features

* **No Installation Required:** It's a single, self-contained HTML/JS file. Just open it in any web browser.
* **Interactive Visual UI:** Easy-to-use dropdowns and inputs mapped perfectly to the game's 21 perimeter pins (Top, Right, and Left edges).
* **Instant Solving:** Uses an optimized constraint satisfaction algorithm to find the solution in **milliseconds**.
* **Built-in Validation:** Automatically checks if your input counts are mathematically consistent before attempting to solve.
* **Clear Output:** Generates a visual hexagonal grid of **Yellow (🟡)** and **Black (⚫)** cells that maps 1:1 with the game board.

---

## 🚀 How to Use

1. Download or clone this repository.
2. Double-click `buzzled.master.solver.html` to open it in your web browser.
3. Open *Puzzmallow's* daily **Buzzled Master** puzzle.
4. Copy the 21 pins from the game into the solver:
   - Select the color (**Yellow** or **Black**) and enter the number for each pin.
   - *Tip: The UI is broken down into Top, Right/Bottom-Right, and Left/Bottom-Left to make mapping easy.*
5. Click **Solve Puzzle**.
6. Click the hexes on the Buzzled website to match the Yellow/Black output grid to win the daily challenge!

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
