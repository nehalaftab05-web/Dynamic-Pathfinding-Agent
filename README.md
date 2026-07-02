# Dynamic-Pathfinding-Agent
<img width="959" height="490" alt="image" src="https://github.com/user-attachments/assets/919261d5-d915-4bae-a700-0db106b1cb48" />
<img width="959" height="472" alt="image" src="https://github.com/user-attachments/assets/502d0b18-7310-4946-a1fd-0c3a85ee7dcd" />
<img width="959" height="482" alt="image" src="https://github.com/user-attachments/assets/d840e284-4375-4cd1-a30b-662017556939" />
# 🧭 Dynamic Pathfinding Agent — Premium UI Edition with tkinter gui

A desktop pathfinding visualizer built entirely with Python's standard `tkinter` library — no external dependencies. It lets you draw walls on a grid, place a start and goal, and watch **A\*** or **Greedy Best-First Search** explore the space in real time. Obstacles can spawn dynamically while the agent is mid-journey, forcing the agent to detect the blockage and **replan its route live**.

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [How It Works — High-Level Flow](#-how-it-works--high-level-flow)
4. [Installation & Running](#-installation--running)
5. [Project Structure](#-project-structure)
6. [Design System (Tokens)](#-design-system-tokens)
7. [Algorithms Explained](#-algorithms-explained)
8. [Custom UI Widgets](#-custom-ui-widgets)
9. [Application Architecture — `PathfindingApp`](#-application-architecture--pathfindingapp)
10. [Controls Reference](#-controls-reference)
11. [Complexity Analysis](#-complexity-analysis)
12. [Design Notes & Limitations](#-design-notes--limitations)
13. [Future Improvements](#-future-improvements)
14. [Requirements](#-requirements)
15. [License](#-license)

---

## 🔍 Overview

This project is a single-file Python application (`main.py`) that combines:

- **Search algorithms** — A* and Greedy Best-First Search, each pluggable with either a Manhattan or Euclidean heuristic.
- **A hand-built dark-themed UI** — every widget (buttons, toggles, sliders, metric cards, legends) is a custom class built on top of raw `tkinter.Frame`/`tkinter.Label`/`tkinter.Canvas`, since stock Tk widgets don't support this level of styling.
- **An interactive grid editor** — click-and-drag to paint walls, relocate the start/goal nodes, or generate a randomized maze.
- **Dynamic replanning** — while the agent walks its path, new walls can randomly appear; if they block the remaining route, the agent detects it and re-runs the search from its current position.

The result behaves like a small "robot navigation" simulator: you set up the environment, hit **Start Search**, and watch the algorithm reason about the grid — first exploring, then walking, and (optionally) reacting to a changing world.

---

## ✨ Features

| Category | Details |
|---|---|
| **Algorithms** | A* Search, Greedy Best-First Search |
| **Heuristics** | Manhattan distance, Euclidean distance |
| **Grid editing** | Click to toggle walls, drag-paint, right-click to erase, resizable rows/columns (5–50 / 5–60) |
| **Maze generation** | Randomized wall density (10%–60%) via one click |
| **Dynamic obstacles** | Configurable spawn probability; walls can appear mid-run |
| **Live replanning** | Agent detects a blocked path and automatically recalculates a new one |
| **Real-time metrics** | Nodes visited, path cost, search time (ms), replan count |
| **Animated visualization** | Explored ("visited") nodes reveal progressively, followed by the highlighted final path and a moving agent marker |
| **Status system** | Color-coded status pill/label reflecting `READY`, `SEARCHING…`, `ANIMATING`, `RE-PLAN #n`, `DONE`, `FAILED`, `STOPPED` |
| **No dependencies** | Pure standard library: `tkinter`, `heapq`, `random`, `time`, `math`, `collections` |

---

## 🔄 How It Works — High-Level Flow

```
┌────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Edit Grid │ ──▶ │  Start Search │ ──▶ │  Run A* / GBFS    │
│ (walls,    │     │  (button)     │     │  synchronously,   │
│  start,    │     │               │     │  collect visited  │
│  goal)     │     │               │     │  order + path     │
└────────────┘     └───────────────┘     └─────────┬─────────┘
                                                     │
                    ┌────────────────────────────────┘
                    ▼
        ┌────────────────────┐     ┌─────────────────────┐     ┌───────────────┐
        │ Animate "visited"  │ ──▶ │ Draw final path,     │ ──▶ │ Step agent     │
        │ nodes in batches   │     │ place agent at start │     │ along path     │
        └────────────────────┘     └─────────────────────┘     └───────┬───────┘
                                                                         │
                          ┌──────────────────────────────────────────────┘
                          ▼
              ┌───────────────────────┐        blocked        ┌────────────────┐
              │ Dynamic obstacle spawn │ ───────────────────▶ │ Replan from     │
              │ check each tick        │                       │ current cell    │
              └───────────┬───────────┘                        └────────┬────────┘
                          │ clear                                        │
                          ▼                                              ▼
                  ┌───────────────┐                             back into agent loop
                  │ Reached Goal? │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │ DONE / FAILED │
                  └───────────────┘
```

---

## 🚀 Installation & Running

No external packages are required — `tkinter` ships with most standard Python installations.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/dynamic-pathfinding-agent.git
cd dynamic-pathfinding-agent

# 2. (Linux only, if tkinter isn't already installed)
sudo apt-get install python3-tk

# 3. Run the application
python main.py
```

A window (minimum size `980×640`) will open titled **"Dynamic Pathfinding Agent."**

---

## 📁 Project Structure

```
.
├── main.py        # Entire application (algorithms + UI + app logic)
└── README.md
```

Everything lives in one file, organized internally into four clearly commented sections:

1. **Design Tokens** — colors, fonts, sizing constants
2. **Algorithms** — heuristics, neighbor generation, A*, GBFS
3. **Custom Widgets** — reusable Tk-based UI components
4. **Main Application** — the `PathfindingApp` class and entry point

---

## 🎨 Design System (Tokens)

All visual styling is centralized at the top of the file as module-level constants, which is what makes the dark theme consistent across every widget.

| Group | Constants | Purpose |
|---|---|---|
| **Surfaces** | `BG`, `SURFACE`, `SURFACE2`, `BORDER` | Background layers, from outermost window to nested cards |
| **Accents** | `ACCENT` (purple), `ACCENT2` (teal), `ACCENT3` (pink) | Used to color-code algorithm choice, heuristic choice, and highlighted metrics |
| **Text** | `TEXT`, `TEXT_DIM`, `TEXT_BRIGHT` | Primary, muted, and emphasized text colors |
| **Grid cell colors** | `C_EMPTY`, `C_WALL`, `C_WALL_BDR`, `C_START`, `C_GOAL`, `C_FRONTIER`, `C_VISITED`, `C_PATH`, `C_AGENT`, `C_GRID` | One color per possible cell state — this is effectively the visual "legend" of the app |
| **Layout** | `CELL_SIZE = 26`, `GAP = 2` | Pixel size of each grid square and the spacing between squares |
| **Typography** | `FONT_TITLE`, `FONT_LABEL`, `FONT_SMALL`, `FONT_METRIC`, `FONT_MKEY`, `FONT_BTN`, `FONT_HEAD` | A monospaced ("Courier") type scale used throughout, giving the app a terminal/technical aesthetic |

Because every widget class pulls its colors from these shared constants instead of hardcoding hex values, the whole theme can be changed by editing this one block.

---

## 🧠 Algorithms Explained

### Heuristics

```python
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])
```

- **Manhattan distance** sums the horizontal and vertical distance between two cells. It's the *natural* heuristic here because the agent can only move in 4 directions (up/down/left/right) — it's admissible and tight for this movement model.
- **Euclidean distance** is the straight-line ("as the crow flies") distance. It's still admissible (never overestimates), but looser than Manhattan for a 4-directional grid, so A* using it typically explores a few more nodes.

### Neighbor Expansion

```python
def get_neighbors(node, rows, cols, grid):
    r, c = node
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            yield (nr, nc)
```

A generator that yields the (up to) four orthogonal neighbors of a cell, filtering out anything off-grid or marked as a wall (`grid[r][c] == 1`). No diagonal movement is allowed.

### Path Reconstruction

```python
def reconstruct(came_from, goal):
    path, cur = [], goal
    while cur is not None:
        path.append(cur); cur = came_from[cur]
    path.reverse(); return path
```

Both search functions build a `came_from` dictionary mapping each visited node to the node it was reached from. Once the goal is found, `reconstruct` walks backward from goal → start following those parent pointers, then reverses the list into start → goal order.

### A* Search

```python
def run_astar(grid, rows, cols, start, goal, hfn):
    heap = [(hfn(start,goal), 0, start)]
    g = defaultdict(lambda: float('inf')); g[start] = 0
    came_from = {start: None}; visited = []
    while heap:
        f, gc, cur = heapq.heappop(heap)
        if gc > g[cur]: continue
        if cur == goal: return reconstruct(came_from, goal), visited
        visited.append(cur)
        for nb in get_neighbors(cur, rows, cols, grid):
            ng = g[cur]+1
            if ng < g[nb]:
                g[nb]=ng; came_from[nb]=cur
                heapq.heappush(heap, (ng+hfn(nb,goal), ng, nb))
    return None, visited
```

Standard A* using Python's `heapq` as a priority queue, ordered by `f = g + h`:

- `g` is a `defaultdict` initialized to infinity, so any unseen node is automatically treated as unreachable until proven otherwise.
- Because `heapq` has no built-in "decrease-key" operation, the algorithm uses **lazy deletion**: stale (outdated) heap entries are simply skipped via `if gc > g[cur]: continue` rather than removed from the heap directly. This is a standard, efficient trick for Python implementations of Dijkstra/A*.
- Every popped node (except when skipped as stale) is appended to `visited` — this list isn't used for the algorithm's correctness, but purely to drive the **animation**, letting the UI replay the exact order in which A* explored the grid.
- Each edge has a uniform cost of `1` (`ng = g[cur] + 1`), consistent with a 4-directional unweighted grid.

### Greedy Best-First Search (GBFS)

```python
def run_gbfs(grid, rows, cols, start, goal, hfn):
    heap = [(hfn(start,goal), start)]
    came_from = {start: None}; visited = []
    while heap:
        _, cur = heapq.heappop(heap)
        if cur == goal: return reconstruct(came_from, goal), visited
        visited.append(cur)
        for nb in get_neighbors(cur, rows, cols, grid):
            if nb not in came_from:
                came_from[nb]=cur
                heapq.heappush(heap, (hfn(nb,goal), nb))
    return None, visited
```

GBFS orders the priority queue **purely by the heuristic** `h(n)` — it ignores the actual cost accumulated so far (`g`). This makes it faster in open areas (it "beelines" toward the goal), but **not guaranteed optimal**: it can walk into a heuristically-promising dead end and take a much longer route than A* would. A node is only ever added to `came_from` once (`if nb not in came_from`), so GBFS never revisits or improves a node's parent — another reason its output path can be suboptimal compared to A*.

### A* vs. GBFS — Practical Difference in This App

| | A* | GBFS |
|---|---|---|
| Ordered by | `g + h` (cost so far + estimate) | `h` only (estimate) |
| Path optimality | Always shortest (with admissible heuristic) | Not guaranteed |
| Typical node count | Higher (more thorough) | Lower (faster but riskier) |
| Best for | Guaranteed shortest path | Quick approximate routing |

---

## 🧩 Custom UI Widgets

Tkinter's built-in `Button`, `Checkbutton`, and `Scale` widgets are notoriously hard to restyle (especially on Windows/macOS, where native theming overrides colors). To get the dark, "pill-shaped," modern look, this project builds six reusable components from lower-level primitives (`Label`, `Frame`, `Canvas`).

### `FlatButton(tk.Label)`
A clickable, pill-styled button implemented as a `Label` (chosen over `Button` for more reliable cross-platform color control).
- Binds `<Enter>` / `<Leave>` to lighten/restore the background color on hover, and `<Button-1>` to fire the given `command`.
- `_lighten(hx)` manually brightens a hex color by adding `35` to each RGB channel (capped at 255) to compute the hover shade — no external color library needed.
- `set_enabled(bool)` grays the button out and disables the hand cursor when a search is running (e.g. the "Start" button is disabled while a search is already in progress).

### `ToggleGroup(tk.Frame)`
A segmented control (like an iOS-style switch with more than two options) used for **Algorithm** (A*/GBFS), **Heuristic** (Manhattan/Euclidean), and **Edit Mode** (Wall/Start/Goal).
- Takes a list of `(value, label)` pairs and a shared `tk.StringVar`.
- Clicking any option sets the variable; a `trace_add("write", ...)` callback automatically re-styles all buttons whenever the variable changes — so the active option is always highlighted with its assigned color and the rest stay dimmed.

### `SliderCard(tk.Frame)`
A labeled `tk.Scale` with a live-updating value readout, used for **Obstacle Density**, **Spawn Probability**, and **Animation Speed**.
- Accepts a `fmt` string (e.g. `"{:.0%}"` for percentages, `"{:.3f}"` for small probabilities) so the same component can display very differently-scaled numbers correctly.
- The slider's `command` callback updates the label text on every drag tick, giving instant visual feedback.

### `MetricCard(tk.Frame)`
A small stat display: a thin colored top border, a large monospaced number bound to a `StringVar`, and a dim caption underneath. Four of these make up the metrics bar: **Nodes Visited**, **Path Cost**, **Time (ms)**, **Re-plans**.

### `SectionHeader(tk.Frame)`
A simple pattern used repeatedly inside the sidebar cards: an uppercase label followed by a horizontal divider line that stretches to fill remaining space — a lightweight way to visually separate control groups without a full bordered box.

### `LegendDot(tk.Frame)`
A small colored circle (drawn on a tiny `Canvas`) next to a text label, used to build the **Legend** panel that explains what each grid color means (Start, Goal, Agent, Visited, Frontier, Final Path, Wall).

---

## 🏗️ Application Architecture — `PathfindingApp`

The entire UI and simulation logic live inside one class, `PathfindingApp`, instantiated once in `main()` with the root Tk window.

### State & Variables (`__init__`)

**Grid state**
- `rows`, `cols` — grid dimensions (default `22 × 32`)
- `grid` — a 2D list of `0`/`1` (`0` = empty, `1` = wall)
- `start`, `goal` — `(row, col)` tuples, default to opposite corners
- `path`, `visited` — results of the last search
- `agent_pos`, `agent_step` — current animated position and index along `path`

**Runtime/animation control**
- `running` — guards against starting a second search while one is active
- `_draw_job`, `_agent_job` — handles to scheduled `root.after(...)` callbacks, so they can be cancelled on stop/reset
- `_anim_index` — progress counter for the "visited nodes" reveal animation
- `_replan_count` — how many times the agent has replanned mid-journey

**User-configurable `tk` variables**
| Variable | Type | Default | Meaning |
|---|---|---|---|
| `algorithm` | `StringVar` | `"astar"` | `"astar"` or `"gbfs"` |
| `heuristic` | `StringVar` | `"manhattan"` | `"manhattan"` or `"euclidean"` |
| `edit_mode` | `StringVar` | `"wall"` | What clicking the grid does: `"wall"`, `"start"`, or `"goal"` |
| `obstacle_density` | `DoubleVar` | `0.28` | Wall probability used by *Generate Maze* |
| `dynamic_prob` | `DoubleVar` | `0.015` | Per-cell, per-tick probability of a new wall spawning during dynamic mode |
| `anim_speed` | `IntVar` | `30` | Milliseconds between agent movement ticks |
| `dyn_var` | `BooleanVar` | `False` | Whether dynamic obstacle spawning is enabled |

**Metric display `StringVar`s** — `nodes_var`, `cost_var`, `time_var`, `replan_var`, `status_var`, all bound directly to labels so updating the variable automatically updates the UI.

### Layout Construction

The UI is built top-down through a chain of `_build_*` methods, all called once from `_build_layout()`:

- **`_build_titlebar`** — app name, a small colored indicator dot, a subtitle listing supported algorithms, and a color-coded status "pill" on the right.
- **`_card(parent, title)`** — a small helper factory used everywhere else: wraps content in a padded, surface-colored `Frame`, optionally topped with a `SectionHeader`. This is what gives every sidebar panel a consistent "card" look with one line of code.
- **`_build_sidebar`** — assembles the left-hand control column out of cards: *Algorithm*, *Edit Mode*, *Grid Size* (spinboxes + Apply/Generate Maze/Clear buttons + density slider), *Dynamic Obstacles* (custom toggle switch + spawn-probability slider), *Animation Speed*, and *Legend*.
- **`_draw_toggle` / `_toggle_dynamic`** — since Tkinter has no native iOS-style switch, the Dynamic Obstacles on/off control is hand-drawn on a small `Canvas`: an oval track plus a circular "knob" whose x-position shifts left/right depending on `dyn_var`.
- **`_build_canvas_area`** — assembles the right-hand side: the action bar, the metrics bar, and the bordered grid `Canvas` itself, wiring up mouse bindings (`<Button-1>`, `<B1-Motion>`, `<Button-3>`).
- **`_build_action_bar`** — the **Start Search**, **Stop**, and **Reset** buttons, plus a live status readout.
- **`_build_metrics_bar`** — the four `MetricCard`s laid out horizontally.

### Canvas Rendering Pipeline

- **`_recalc_canvas`** — computes the pixel width/height needed for the canvas from `rows`/`cols`/`CELL_SIZE`/`GAP` and resizes the widget accordingly (called on startup and after a grid resize).
- **`draw_grid`** — a full repaint: clears the canvas and calls `_draw_cell` for every `(r, c)`.
- **`_draw_cell(r, c)`** — draws a single cell, tagged uniquely as `f"cell_{r}_{c}"` so it can be redrawn independently later without touching the rest of the canvas. Priority order for what gets drawn:
  1. **Agent's current position** → path-colored background + a white circular marker
  2. **Start** → green square labeled `"S"`
  3. **Goal** → red/pink square labeled `"G"`
  4. **Wall** (`grid[r][c] == 1`) → filled with border outline
  5. Otherwise, checked against three membership sets (`_path_set`, `_visited_set`, `_frontier_set`) to decide whether it should render as final path, explored/visited, or frontier — falling back to the empty-cell color with a subtle grid outline.
- **`_refresh_cell(r, c)`** — a thin alias around `_draw_cell`, used throughout the app for targeted, efficient single-cell updates (e.g. as the agent moves) instead of redrawing the entire grid every frame.

### User Interaction (Mouse Handling)

- **`_cell_from_event(event)`** — converts a raw pixel `(x, y)` click position into a `(row, col)` grid coordinate, returning `None` if outside bounds.
- **`on_click` / `on_drag`** — both route through `_apply_edit`, letting the user paint continuously by holding and dragging the mouse (disabled while `running`).
- **`on_right_click`** — erases a wall at the clicked cell (unless it's the start/goal).
- **`_apply_edit(cell)`** — behavior depends on `edit_mode`:
  - `"wall"` → toggles the cell between `0` and `1` (`1 - grid[r][c]`)
  - `"start"` → moves the start marker to the clicked cell, refreshing both the old and new cell
  - `"goal"` → same, for the goal marker

### Grid Management

- **`resize_grid`** — stops any active search, reads and clamps the row/column spinbox values (`5–50` rows, `5–60` columns), rebuilds the grid array from scratch, resets start/goal to opposite corners, and redraws.
- **`generate_maze`** — stops any active search, then for every non-start/goal cell rolls a random number against `obstacle_density` to decide if it becomes a wall.
- **`clear_grid`** — resets the grid to all-empty.
- **`_reset_sets`** — clears the three rendering sets (`_path_set`, `_visited_set`, `_frontier_set`).
- **`_reset_all`** — a broader reset combining `_reset_sets` with clearing `path`, `visited`, `agent_pos`, and `_replan_count`.

### Search Execution & Animation

- **`start_search`** — the entry point triggered by the **Start Search** button:
  1. Resets all visualization state and metric displays, sets status to `SEARCHING…`.
  2. Selects the heuristic function and search function based on the current `ToggleGroup` selections.
  3. Runs the chosen algorithm **synchronously**, timed with `time.perf_counter()`.
  4. Updates the *Nodes Visited* and *Time* metrics immediately.
  5. If no path exists, shows a `messagebox.showwarning` and stops here.
  6. Otherwise sets the *Path Cost* metric, disables the Start button, enables Stop, and kicks off `_animate_visited`.

- **`_animate_visited`** — reveals the `visited` list progressively rather than all at once. It computes a `batch` size as `len(visited) // 80`, so regardless of how large the grid or how many nodes were explored, the reveal always takes roughly 80 animation frames — keeping playback speed visually consistent across grid sizes. Each frame is scheduled via `root.after(speed // 5, ...)`.

- **`_show_path_and_move`** — once the explored-node animation finishes, highlights every cell in the final `path`, places the agent at `start`, and calls `_move_agent`.

- **`_move_agent`** — the per-tick agent step function, and the heart of the dynamic-replanning feature:
  1. **If dynamic obstacles are enabled**, iterates the entire grid and, for each empty cell (excluding start/goal/agent), rolls against `dynamic_prob` to possibly spawn a new wall — then checks `_path_blocked()`. If the remaining path is now obstructed, it calls `_replan()` and returns early.
  2. Otherwise, advances the agent one cell forward along `path`, clears the previous cell's highlight, refreshes both cells, and checks for arrival at `goal` (→ `_finish()`).
  3. If not yet finished, schedules the next tick via `root.after(speed, self._move_agent)`.

- **`_path_blocked`** — scans the *remaining* (unwalked) portion of `path` and returns `True` if any of those cells have since become a wall.

- **`_replan`** — re-runs the currently selected algorithm from the agent's **current position** (not the original start) to the goal:
  - Clears the old path highlighting.
  - If no path can be found anymore, sets status to `PATH BLOCKED!` and calls `_finish(failed=True)`.
  - Otherwise increments `_replan_count`, updates all four metrics, re-highlights the new path, and resumes `_move_agent` on the next tick.

- **`_finish(failed=False)`** — re-enables the Start button, disables Stop, and sets the status to either `✓ DONE!` (green) or `✕ FAILED` (red).

### Status & Lifecycle Management

- **`stop_search`** — cancels any pending `root.after` callbacks (`_draw_job`, `_agent_job`), re-enables the Start button, and sets status to `STOPPED`. Called defensively at the start of every grid-editing action so edits never race with an in-progress animation.
- **`reset_search`** — combines `stop_search` with a full visualization/metric reset and redraw, restoring the grid to `READY`.
- **`_set_status(text, color)`** — the single source of truth for status display; updates both the title-bar "pill" and the action-bar status label with matching text and color.

### Entry Point

```python
if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(980, 640)
    app = PathfindingApp(root)
    root.mainloop()
```

Standard Tkinter bootstrap: create the root window, enforce a minimum size so the layout doesn't collapse, instantiate the app, and hand control to Tkinter's event loop.

---

## 🎮 Controls Reference

| Action | How |
|---|---|
| Toggle a wall | Left-click a cell (Edit Mode: **Wall**) |
| Paint multiple walls | Left-click and drag |
| Erase a wall | Right-click a cell |
| Move the start node | Switch Edit Mode to **Start**, then click a cell |
| Move the goal node | Switch Edit Mode to **Goal**, then click a cell |
| Change grid size | Edit Rows/Cols spinboxes → **Apply Size** |
| Randomize obstacles | Adjust **Obstacle Density** slider → **Generate Maze** |
| Clear all walls | **Clear** button |
| Switch algorithm | Algorithm toggle: **A\*** / **GBFS** |
| Switch heuristic | Heuristic toggle: **Manhattan** / **Euclidean** |
| Enable live obstacle spawning | Flip the **Dynamic Obstacles** switch, tune **Spawn Probability** |
| Adjust playback speed | **Animation Speed** slider (lower = faster) |
| Run the search | **▶ START SEARCH** |
| Halt mid-animation | **⏹ STOP** |
| Clear results, keep grid | **↺ Reset** |

---

## 📊 Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Optimal? |
|---|---|---|---|
| A* | O(b^d) worst case; much better in practice with an informed heuristic | O(b^d) (stores frontier + `g`-scores) | ✅ Yes (with an admissible heuristic, which both Manhattan and Euclidean are here) |
| GBFS | O(b^d) worst case | O(b^d) | ❌ Not guaranteed |

Where `b` is the branching factor (up to 4, since movement is 4-directional) and `d` is the depth of the solution in the search tree. In practice, on the grid sizes this app supports (up to 50×60 = 3,000 cells), both algorithms run in milliseconds, which is why the search itself is executed synchronously (not threaded) — only the *visualization* of the result is animated afterward.

---

## 🛠️ Design Notes & Limitations

- **Movement model**: 4-directional only (no diagonals), consistent with how `get_neighbors` and both heuristics are defined.
- **Synchronous search**: the algorithm runs to completion before any animation starts. What you see animate is a **replay** of the already-computed `visited` order, not the live search — this keeps the algorithm code simple and decoupled from the UI/animation timing.
- **Dynamic obstacles are agent-relative**: new walls can appear anywhere except on the start, goal, or the agent's current cell, but they *can* appear on already-visited or already-highlighted path cells, which is exactly what triggers a replan.
- **Lazy-deletion priority queue**: both `heapq`-based searches tolerate duplicate/stale entries in the heap rather than implementing a full decrease-key, which is the idiomatic approach in Python since `heapq` has no native support for it.
- **No persistence**: grid layouts, settings, and results are in-memory only and reset when the app closes.

---

## 🔮 Future Improvements

- Diagonal movement (8-directional) with an octile-distance heuristic
- Weighted terrain (variable-cost cells instead of binary wall/empty)
- Dijkstra and Bidirectional Search as additional algorithm options
- Asynchronous/threaded search so extremely large grids don't briefly freeze the UI
- Exporting the visualization as a GIF/video
- Side-by-side comparison mode (run A* and GBFS on the same grid simultaneously)
- Save/load custom grid layouts to disk

---

## 📦 Requirements

- Python 3.8+
- `tkinter` (included with most standard Python distributions; on some Linux distros install separately via `python3-tk`)

No third-party packages are required.

---

## 📄 License

This project is intended for educational and academic purposes.
