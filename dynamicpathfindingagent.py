
"""
Dynamic Pathfinding Agent — Premium UI Edition
Algorithms: A* and Greedy Best-First Search
Heuristics: Manhattan, Euclidean
Features: Dynamic obstacles, interactive editor, real-time metrics
"""

import tkinter as tk
from tkinter import messagebox
import heapq, random, time, math
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════
#  DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════
BG          = "#0d0d14"
SURFACE     = "#13131f"
SURFACE2    = "#1a1a2e"
BORDER      = "#2a2a45"
ACCENT      = "#7c6af7"
ACCENT2     = "#5eead4"
ACCENT3     = "#f472b6"
TEXT        = "#e2e8f0"
TEXT_DIM    = "#64748b"
TEXT_BRIGHT = "#f8fafc"

C_EMPTY    = "#111120"
C_WALL     = "#2d2d4e"
C_WALL_BDR = "#3d3d6e"
C_START    = "#10b981"
C_GOAL     = "#f43f5e"
C_FRONTIER = "#fbbf24"
C_VISITED  = "#3b82f6"
C_PATH     = "#a78bfa"
C_AGENT    = "#ffffff"
C_GRID     = "#1e1e35"

CELL_SIZE = 26
GAP       = 2

FONT_TITLE  = ("Courier", 15, "bold")
FONT_LABEL  = ("Courier", 9)
FONT_SMALL  = ("Courier", 8)
FONT_METRIC = ("Courier", 18, "bold")
FONT_MKEY   = ("Courier", 8)
FONT_BTN    = ("Courier", 9, "bold")
FONT_HEAD   = ("Courier", 10, "bold")

# ══════════════════════════════════════════════════════════════════
#  ALGORITHMS
# ══════════════════════════════════════════════════════════════════

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def get_neighbors(node, rows, cols, grid):
    r, c = node
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            yield (nr, nc)

def reconstruct(came_from, goal):
    path, cur = [], goal
    while cur is not None:
        path.append(cur); cur = came_from[cur]
    path.reverse(); return path

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

# ══════════════════════════════════════════════════════════════════
#  CUSTOM WIDGETS
# ══════════════════════════════════════════════════════════════════

class FlatButton(tk.Label):
    """Pill-shaped button using tk.Label for reliable geometry management."""
    def __init__(self, parent, text, command, color=ACCENT,
                 text_color=TEXT_BRIGHT, width=140, height=34,
                 font=FONT_BTN, **kw):
        # Convert pixel width to approximate char width for Label
        self._color  = color
        self._hcolor = self._lighten(color)
        self._cmd    = command
        self._enabled = True
        self._tc     = text_color
        self._base_color = color

        super().__init__(
            parent, text=text, font=font,
            bg=color, fg=text_color,
            padx=10, pady=6,
            cursor="hand2", relief=tk.FLAT,
            width=max(1, width // 8),
            **kw
        )
        self.bind("<Enter>",    lambda e: self._on_enter())
        self.bind("<Leave>",    lambda e: self._on_leave())
        self.bind("<Button-1>", lambda e: self._on_click())

    def _on_enter(self):
        if self._enabled:
            self.config(bg=self._hcolor)

    def _on_leave(self):
        self.config(bg=self._color if self._enabled else "#333344")

    def _on_click(self):
        if self._enabled:
            self._cmd()

    def _lighten(self, hx):
        r,g,b = int(hx[1:3],16), int(hx[3:5],16), int(hx[5:7],16)
        return f"#{min(255,r+35):02x}{min(255,g+35):02x}{min(255,b+35):02x}"

    def set_enabled(self, enabled):
        self._enabled = enabled
        if enabled:
            self.config(bg=self._color, fg=self._tc, cursor="hand2")
        else:
            self.config(bg="#333344", fg="#666677", cursor="")


class ToggleGroup(tk.Frame):
    def __init__(self, parent, options, variable, colors=None, **kw):
        super().__init__(parent, bg=SURFACE2, padx=2, pady=2, **kw)
        self._var = variable
        self._btns = {}
        self._colors = colors or {}
        for val, label in options:
            btn = tk.Label(self, text=label, font=FONT_LABEL,
                            cursor="hand2", padx=10, pady=4,
                            bg=SURFACE2, fg=TEXT_DIM)
            btn.pack(side=tk.LEFT, padx=1)
            btn.bind("<Button-1>", lambda e, v=val: self._var.set(v))
            btn.bind("<Enter>",    lambda e, b=btn, v=val: self._hover(b,v))
            btn.bind("<Leave>",    lambda e: self._refresh())
            self._btns[val] = btn
        variable.trace_add("write", lambda *a: self._refresh())
        self._refresh()

    def _hover(self, btn, val):
        if self._var.get() != val:
            btn.config(fg=TEXT, bg=BORDER)

    def _refresh(self):
        cur = self._var.get()
        for val, btn in self._btns.items():
            if val == cur:
                btn.config(bg=self._colors.get(val, ACCENT), fg=TEXT_BRIGHT)
            else:
                btn.config(bg=SURFACE2, fg=TEXT_DIM)


class SliderCard(tk.Frame):
    def __init__(self, parent, label, variable, from_, to,
                 resolution, fmt="{:.2f}", color=ACCENT, **kw):
        super().__init__(parent, bg=SURFACE, **kw)
        self._fmt = fmt
        row = tk.Frame(self, bg=SURFACE)
        row.pack(fill=tk.X, padx=8, pady=(6,0))
        tk.Label(row, text=label, font=FONT_MKEY, bg=SURFACE, fg=TEXT_DIM).pack(side=tk.LEFT)
        self._lbl = tk.Label(row, text=fmt.format(variable.get()),
                              font=FONT_LABEL, bg=SURFACE, fg=color)
        self._lbl.pack(side=tk.RIGHT)
        tk.Scale(self, variable=variable, from_=from_, to=to,
                 resolution=resolution, orient=tk.HORIZONTAL, length=180,
                 showvalue=False, bg=SURFACE, fg=color,
                 highlightthickness=0, troughcolor=SURFACE2,
                 activebackground=color, sliderrelief=tk.FLAT, bd=0,
                 command=lambda v: self._lbl.config(text=fmt.format(float(v)))
                 ).pack(padx=8, pady=(0,6))


class MetricCard(tk.Frame):
    def __init__(self, parent, label, var, color=ACCENT2, **kw):
        super().__init__(parent, bg=SURFACE, **kw)
        tk.Frame(self, bg=color, height=3).pack(fill=tk.X)
        tk.Label(self, textvariable=var, font=FONT_METRIC,
                  bg=SURFACE, fg=color).pack(pady=(6,0))
        tk.Label(self, text=label, font=FONT_MKEY,
                  bg=SURFACE, fg=TEXT_DIM).pack(pady=(0,8))


class SectionHeader(tk.Frame):
    def __init__(self, parent, title, **kw):
        bg = kw.pop("bg", SURFACE)
        super().__init__(parent, bg=bg, **kw)
        tk.Label(self, text=title.upper(), font=FONT_MKEY,
                  bg=bg, fg=TEXT_DIM).pack(side=tk.LEFT)
        tk.Frame(self, bg=BORDER, height=1).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(6,0), pady=6)


class LegendDot(tk.Frame):
    def __init__(self, parent, color, label, **kw):
        bg = kw.pop("bg", SURFACE)
        super().__init__(parent, bg=bg, **kw)
        c = tk.Canvas(self, width=12, height=12, bg=bg, highlightthickness=0)
        c.create_oval(1,1,11,11, fill=color, outline="")
        c.pack(side=tk.LEFT)
        tk.Label(self, text=label, font=FONT_SMALL, bg=bg, fg=TEXT_DIM).pack(side=tk.LEFT, padx=4)


# ══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.rows = 22
        self.cols = 32
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self.start = (0, 0)
        self.goal  = (self.rows-1, self.cols-1)
        self.path  = []
        self.visited = []
        self.agent_pos  = None
        self.agent_step = 0
        self.running = False
        self._draw_job  = None
        self._agent_job = None
        self._anim_index = 0
        self._replan_count = 0

        self.algorithm        = tk.StringVar(value="astar")
        self.heuristic        = tk.StringVar(value="manhattan")
        self.edit_mode        = tk.StringVar(value="wall")
        self.obstacle_density = tk.DoubleVar(value=0.28)
        self.dynamic_prob     = tk.DoubleVar(value=0.015)
        self.anim_speed       = tk.IntVar(value=30)
        self.dyn_var          = tk.BooleanVar(value=False)

        self.nodes_var  = tk.StringVar(value="—")
        self.cost_var   = tk.StringVar(value="—")
        self.time_var   = tk.StringVar(value="—")
        self.replan_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="READY")

        self._reset_sets()
        self._build_layout()
        self.draw_grid()

    # ─────────────────────────────────────────────────────────────
    #  LAYOUT BUILDER
    # ─────────────────────────────────────────────────────────────

    def _build_layout(self):
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        self._build_titlebar(outer)
        content = tk.Frame(outer, bg=BG)
        content.pack(fill=tk.BOTH, expand=True, pady=(8,0))
        self._build_sidebar(content)
        self._build_canvas_area(content)

    def _build_titlebar(self, parent):
        bar = tk.Frame(parent, bg=SURFACE, pady=10, padx=16)
        bar.pack(fill=tk.X, pady=(0,8))

        dot = tk.Canvas(bar, width=10, height=10, bg=SURFACE, highlightthickness=0)
        dot.create_oval(0,0,10,10, fill=ACCENT, outline="")
        dot.pack(side=tk.LEFT, padx=(0,10))

        tk.Label(bar, text="PATHFINDING AGENT", font=FONT_TITLE,
                  bg=SURFACE, fg=TEXT_BRIGHT).pack(side=tk.LEFT)

        tk.Label(bar, text="A*  •  GBFS  •  Manhattan  •  Euclidean  •  Dynamic Re-planning",
                  font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM).pack(side=tk.LEFT, padx=16)

        pill_frame = tk.Frame(bar, bg=SURFACE)
        pill_frame.pack(side=tk.RIGHT)
        self._status_pill = tk.Label(pill_frame, textvariable=self.status_var,
                                      font=FONT_BTN, bg=ACCENT, fg=TEXT_BRIGHT,
                                      padx=14, pady=4)
        self._status_pill.pack()

    def _card(self, parent, title=None):
        wrapper = tk.Frame(parent, bg=BG, pady=3)
        wrapper.pack(fill=tk.X)
        card = tk.Frame(wrapper, bg=SURFACE, padx=12, pady=10)
        card.pack(fill=tk.X)
        if title:
            SectionHeader(card, title, bg=SURFACE).pack(fill=tk.X, pady=(0,8))
        return card

    def _build_sidebar(self, parent):
        self._sidebar = tk.Frame(parent, bg=BG, width=226)
        self._sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        self._sidebar.pack_propagate(False)

        # ── Algorithm ──────────────────────────────
        card = self._card(self._sidebar, "Algorithm")
        ToggleGroup(card, [("astar","A*  Search"), ("gbfs","GBFS")],
                    self.algorithm,
                    colors={"astar": ACCENT, "gbfs": "#0ea5e9"}
                    ).pack(fill=tk.X, pady=(0,8))
        SectionHeader(card, "Heuristic", bg=SURFACE).pack(fill=tk.X, pady=(2,6))
        ToggleGroup(card, [("manhattan","Manhattan"), ("euclidean","Euclidean")],
                    self.heuristic,
                    colors={"manhattan": ACCENT3, "euclidean": ACCENT2}
                    ).pack(fill=tk.X)

        # ── Edit Mode ──────────────────────────────
        card = self._card(self._sidebar, "Edit Mode")
        ToggleGroup(card,
                    [("wall","Wall"), ("start","Start"), ("goal","Goal")],
                    self.edit_mode,
                    colors={"wall":"#475569","start":C_START,"goal":C_GOAL}
                    ).pack(fill=tk.X, pady=(0,6))
        tk.Label(card, text="L-click: place   R-click: erase   Drag: paint",
                  font=FONT_SMALL, bg=SURFACE, fg=TEXT_DIM).pack()

        # ── Grid ───────────────────────────────────
        card = self._card(self._sidebar, "Grid Size")
        size_row = tk.Frame(card, bg=SURFACE)
        size_row.pack(fill=tk.X, pady=(0,6))
        for label, attr, default in [("Rows","row_spin","22"),("Cols","col_spin","32")]:
            box = tk.Frame(size_row, bg=SURFACE)
            box.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            tk.Label(box, text=label, font=FONT_MKEY, bg=SURFACE, fg=TEXT_DIM).pack(anchor="w")
            sp = tk.Spinbox(box, from_=5, to=60, width=5, bg=SURFACE2, fg=TEXT,
                             relief=tk.FLAT, buttonbackground=BORDER,
                             insertbackground=TEXT, highlightthickness=1,
                             highlightcolor=ACCENT, highlightbackground=BORDER,
                             font=FONT_LABEL)
            sp.delete(0, tk.END); sp.insert(0, default)
            sp.pack(fill=tk.X)
            setattr(self, attr, sp)
        _rb = FlatButton(card, "⟳  Apply Size", self.resize_grid, color=BORDER, width=198, height=30)
        _rb.pack(pady=(0,4))
        SliderCard(card, "Obstacle Density", self.obstacle_density,
                   0.1, 0.6, 0.05, fmt="{:.0%}", color=ACCENT3).pack(fill=tk.X, pady=2)
        btn_row = tk.Frame(card, bg=SURFACE)
        btn_row.pack(fill=tk.X, pady=2)
        _bg = FlatButton(btn_row, "⚡ Generate Maze", self.generate_maze, color=ACCENT, width=98, height=30)
        _bg.pack(side=tk.LEFT, padx=(0,2))
        _bc = FlatButton(btn_row, "✕ Clear", self.clear_grid, color="#475569", width=96, height=30)
        _bc.pack(side=tk.LEFT)

        # ── Dynamic Mode ───────────────────────────
        card = self._card(self._sidebar, "Dynamic Obstacles")
        toggle_row = tk.Frame(card, bg=SURFACE)
        toggle_row.pack(fill=tk.X, pady=(0,8))
        tk.Label(toggle_row, text="Enable Spawning",
                  font=FONT_LABEL, bg=SURFACE, fg=TEXT).pack(side=tk.LEFT)
        self._dyn_toggle = tk.Canvas(toggle_row, width=42, height=22,
                                      bg=SURFACE, highlightthickness=0, cursor="hand2")
        self._dyn_toggle.pack(side=tk.RIGHT)
        self._dyn_toggle.bind("<Button-1>", self._toggle_dynamic)
        self._draw_toggle()
        SliderCard(card, "Spawn Probability", self.dynamic_prob,
                   0.005, 0.05, 0.005, fmt="{:.3f}", color=ACCENT3).pack(fill=tk.X)

        # ── Speed ──────────────────────────────────
        card = self._card(self._sidebar, "Animation Speed")
        SliderCard(card, "Delay (ms/step)", self.anim_speed,
                   5, 200, 5, fmt="{:.0f} ms", color=ACCENT2).pack(fill=tk.X)

        # ── Legend ─────────────────────────────────
        card = self._card(self._sidebar, "Legend")
        for color, label in [(C_START,"Start Node"),(C_GOAL,"Goal Node"),
                              (C_AGENT,"Agent"),(C_VISITED,"Visited"),
                              (C_FRONTIER,"Frontier"),(C_PATH,"Final Path"),(C_WALL,"Wall")]:
            LegendDot(card, color, label, bg=SURFACE).pack(anchor="w", pady=2)

    def _draw_toggle(self):
        self._dyn_toggle.delete("all")
        on = self.dyn_var.get()
        bg_col = ACCENT if on else BORDER
        self._dyn_toggle.create_oval(0, 2, 40, 20, fill=bg_col, outline="")
        x = 24 if on else 10
        self._dyn_toggle.create_oval(x-7, 4, x+7, 18, fill=TEXT_BRIGHT, outline="")

    def _toggle_dynamic(self, e=None):
        self.dyn_var.set(not self.dyn_var.get())
        self._draw_toggle()

    def _build_canvas_area(self, parent):
        right = tk.Frame(parent, bg=BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._build_action_bar(right)
        self._build_metrics_bar(right)
        # Canvas wrapper with border
        wrap = tk.Frame(right, bg=BORDER, padx=1, pady=1)
        wrap.pack(fill=tk.BOTH, expand=True, pady=(8,0))
        inner = tk.Frame(wrap, bg=C_EMPTY)
        inner.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(inner, bg=C_EMPTY, highlightthickness=0)
        self.canvas.pack(padx=4, pady=4)
        self._recalc_canvas()
        self.canvas.bind("<Button-1>",  self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-3>",  self.on_right_click)

    def _build_action_bar(self, parent):
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill=tk.X, pady=(0,6))

        self._start_btn = FlatButton(
            bar, "▶   START SEARCH", self.start_search,
            color=C_START, text_color="#000", width=180, height=40,
            font=("Courier",10,"bold"))
        self._start_btn.pack(side=tk.LEFT, padx=(0,6))

        self._stop_btn = FlatButton(
            bar, "⏹  STOP", self.stop_search,
            color=C_GOAL, text_color="#fff", width=110, height=40)
        self._stop_btn.pack(side=tk.LEFT, padx=(0,6))
        self._stop_btn.set_enabled(False)

        _rst = FlatButton(bar, "↺  Reset", self.reset_search, color=BORDER, width=110, height=40)
        _rst.pack(side=tk.LEFT)

        # Live status display
        status_card = tk.Frame(bar, bg=SURFACE, padx=14, pady=10)
        status_card.pack(side=tk.RIGHT)
        tk.Label(status_card, text="STATUS", font=FONT_MKEY,
                  bg=SURFACE, fg=TEXT_DIM).pack(side=tk.LEFT, padx=(0,10))
        self._status_lbl = tk.Label(status_card, textvariable=self.status_var,
                                     font=("Courier",10,"bold"),
                                     bg=SURFACE, fg=ACCENT2, width=14, anchor="w")
        self._status_lbl.pack(side=tk.LEFT)

    def _build_metrics_bar(self, parent):
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill=tk.X)
        for label, var, color in [
            ("NODES VISITED", self.nodes_var,  ACCENT),
            ("PATH COST",     self.cost_var,   ACCENT2),
            ("TIME  (ms)",    self.time_var,   ACCENT3),
            ("RE-PLANS",      self.replan_var, "#f59e0b"),
        ]:
            MetricCard(bar, label, var, color).pack(
                side=tk.LEFT, fill=tk.X, expand=True, padx=3)

    # ─────────────────────────────────────────────────────────────
    #  CANVAS RENDERING
    # ─────────────────────────────────────────────────────────────

    def _recalc_canvas(self):
        w = self.cols * (CELL_SIZE + GAP) + GAP
        h = self.rows * (CELL_SIZE + GAP) + GAP
        self.canvas.config(width=w, height=h)

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                self._draw_cell(r, c)

    def _draw_cell(self, r, c):
        x1 = c*(CELL_SIZE+GAP)+GAP
        y1 = r*(CELL_SIZE+GAP)+GAP
        x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
        tag = f"cell_{r}_{c}"
        self.canvas.delete(tag)
        pos = (r, c)

        if pos == self.agent_pos:
            self.canvas.create_rectangle(x1,y1,x2,y2, fill=C_PATH, outline="", tags=tag)
            pad = 5
            self.canvas.create_oval(x1+pad,y1+pad,x2-pad,y2-pad,
                                     fill=C_AGENT, outline="", tags=tag)
        elif pos == self.start:
            self.canvas.create_rectangle(x1,y1,x2,y2, fill=C_START, outline="", tags=tag)
            self.canvas.create_text((x1+x2)//2,(y1+y2)//2, text="S",
                                     fill="#000", font=("Courier",8,"bold"), tags=tag)
        elif pos == self.goal:
            self.canvas.create_rectangle(x1,y1,x2,y2, fill=C_GOAL, outline="", tags=tag)
            self.canvas.create_text((x1+x2)//2,(y1+y2)//2, text="G",
                                     fill="#fff", font=("Courier",8,"bold"), tags=tag)
        elif self.grid[r][c] == 1:
            self.canvas.create_rectangle(x1,y1,x2,y2,
                                          fill=C_WALL, outline=C_WALL_BDR, tags=tag)
        else:
            color = C_EMPTY
            if pos in self._path_set:     color = C_PATH
            elif pos in self._visited_set: color = C_VISITED
            elif pos in self._frontier_set:color = C_FRONTIER
            outline = C_GRID if color == C_EMPTY else ""
            self.canvas.create_rectangle(x1,y1,x2,y2,
                                          fill=color, outline=outline, tags=tag)

    def _refresh_cell(self, r, c):
        self._draw_cell(r, c)

    # ─────────────────────────────────────────────────────────────
    #  INTERACTION
    # ─────────────────────────────────────────────────────────────

    def _cell_from_event(self, event):
        c = event.x // (CELL_SIZE+GAP)
        r = event.y // (CELL_SIZE+GAP)
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return r, c
        return None

    def on_click(self, event):
        if self.running: return
        cell = self._cell_from_event(event)
        if cell: self._apply_edit(cell)

    def on_drag(self, event):
        if self.running: return
        cell = self._cell_from_event(event)
        if cell: self._apply_edit(cell)

    def on_right_click(self, event):
        if self.running: return
        cell = self._cell_from_event(event)
        if cell:
            r, c = cell
            if (r,c) not in (self.start, self.goal):
                self.grid[r][c] = 0
                self._refresh_cell(r, c)

    def _apply_edit(self, cell):
        r, c = cell
        mode = self.edit_mode.get()
        if mode == "wall":
            if (r,c) not in (self.start, self.goal):
                self.grid[r][c] = 1 - self.grid[r][c]
                self._refresh_cell(r, c)
        elif mode == "start":
            old = self.start; self.start = (r,c)
            self.grid[r][c] = 0
            self._refresh_cell(*old); self._refresh_cell(r,c)
        elif mode == "goal":
            old = self.goal; self.goal = (r,c)
            self.grid[r][c] = 0
            self._refresh_cell(*old); self._refresh_cell(r,c)

    # ─────────────────────────────────────────────────────────────
    #  GRID MANAGEMENT
    # ─────────────────────────────────────────────────────────────

    def resize_grid(self):
        self.stop_search()
        try:
            rows = max(5, min(50, int(self.row_spin.get())))
            cols = max(5, min(60, int(self.col_spin.get())))
        except ValueError:
            return
        self.rows, self.cols = rows, cols
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self.start = (0,0); self.goal = (self.rows-1, self.cols-1)
        self._reset_all(); self._recalc_canvas(); self.draw_grid()

    def generate_maze(self):
        self.stop_search()
        d = self.obstacle_density.get()
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) not in (self.start, self.goal):
                    self.grid[r][c] = 1 if random.random() < d else 0
        self._reset_all(); self.draw_grid()

    def clear_grid(self):
        self.stop_search()
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self._reset_all(); self.draw_grid()

    def _reset_sets(self):
        self._path_set     = set()
        self._visited_set  = set()
        self._frontier_set = set()

    def _reset_all(self):
        self._reset_sets()
        self.path=[]; self.visited=[]
        self.agent_pos=None; self._replan_count=0

    # ─────────────────────────────────────────────────────────────
    #  SEARCH & ANIMATION
    # ─────────────────────────────────────────────────────────────

    def start_search(self):
        if self.running: return
        self._reset_sets(); self.path=[]; self.visited=[]
        self.agent_pos=None; self.agent_step=0; self._replan_count=0
        self.nodes_var.set("—"); self.cost_var.set("—")
        self.time_var.set("—"); self.replan_var.set("0")
        self._set_status("SEARCHING…", ACCENT)
        self.draw_grid()

        hfn  = manhattan if self.heuristic.get()=="manhattan" else euclidean
        algo = run_astar  if self.algorithm.get()=="astar"    else run_gbfs

        t0 = time.perf_counter()
        path, visited = algo(self.grid, self.rows, self.cols, self.start, self.goal, hfn)
        elapsed = (time.perf_counter()-t0)*1000

        self.nodes_var.set(str(len(visited)))
        self.time_var.set(f"{elapsed:.1f}")

        if path is None:
            self._set_status("NO PATH!", C_GOAL)
            messagebox.showwarning("No Path Found",
                "No path exists between Start and Goal.\nTry removing some walls.")
            return

        self.cost_var.set(str(len(path)-1))
        self._set_status("ANIMATING", ACCENT2)
        self.visited=visited; self.path=path
        self.running=True
        self._start_btn.set_enabled(False)
        self._stop_btn.set_enabled(True)
        self._anim_index=0
        self._animate_visited()

    def _animate_visited(self):
        if not self.running: return
        speed = self.anim_speed.get()
        batch = max(1, len(self.visited)//80)
        end = min(self._anim_index+batch, len(self.visited))
        for i in range(self._anim_index, end):
            n = self.visited[i]
            if n not in (self.start, self.goal):
                self._visited_set.add(n); self._refresh_cell(*n)
        self._anim_index = end
        if self._anim_index < len(self.visited):
            self._draw_job = self.root.after(speed//5, self._animate_visited)
        else:
            self._show_path_and_move()

    def _show_path_and_move(self):
        for n in self.path:
            if n not in (self.start, self.goal):
                self._path_set.add(n); self._refresh_cell(*n)
        self.agent_step=0; self.agent_pos=self.start
        self._move_agent()

    def _move_agent(self):
        if not self.running: return
        speed = self.anim_speed.get()

        if self.dyn_var.get():
            prob = self.dynamic_prob.get()
            for r in range(self.rows):
                for c in range(self.cols):
                    if random.random() < prob:
                        if (r,c) not in (self.start, self.goal, self.agent_pos):
                            if self.grid[r][c]==0:
                                self.grid[r][c]=1
                                self._path_set.discard((r,c))
                                self._refresh_cell(r,c)
            if self._path_blocked():
                self._replan(); return

        if self.agent_step >= len(self.path):
            self._finish(); return

        prev = self.agent_pos
        self.agent_pos  = self.path[self.agent_step]
        self.agent_step += 1

        if prev and prev not in (self.start, self.goal):
            self._path_set.discard(prev); self._refresh_cell(*prev)
        self._refresh_cell(*self.agent_pos)

        if self.agent_pos == self.goal:
            self._finish(); return

        self._agent_job = self.root.after(speed, self._move_agent)

    def _path_blocked(self):
        for n in self.path[self.agent_step:]:
            if self.grid[n[0]][n[1]]==1: return True
        return False

    def _replan(self):
        hfn  = manhattan if self.heuristic.get()=="manhattan" else euclidean
        algo = run_astar  if self.algorithm.get()=="astar"    else run_gbfs
        cur  = self.agent_pos or self.start

        t0 = time.perf_counter()
        path, visited = algo(self.grid, self.rows, self.cols, cur, self.goal, hfn)
        elapsed = (time.perf_counter()-t0)*1000

        for n in list(self._path_set):
            if n not in (self.start, self.goal): self._refresh_cell(*n)
        self._path_set.clear()

        if path is None:
            self._set_status("PATH BLOCKED!", C_GOAL)
            self._finish(failed=True); return

        self._replan_count += 1
        self.path=path; self.agent_step=1
        self.nodes_var.set(str(len(visited)))
        self.time_var.set(f"{elapsed:.1f}")
        self.cost_var.set(str(len(path)-1))
        self.replan_var.set(str(self._replan_count))
        self._set_status(f"RE-PLAN #{self._replan_count}", "#f59e0b")

        for n in self.path:
            if n not in (self.start, self.goal):
                self._path_set.add(n); self._refresh_cell(*n)

        self._agent_job = self.root.after(self.anim_speed.get(), self._move_agent)

    def _finish(self, failed=False):
        self.running=False
        self._start_btn.set_enabled(True)
        self._stop_btn.set_enabled(False)
        if not failed:
            self._set_status("✓  DONE!", C_START)
            if self.agent_pos: self._refresh_cell(*self.agent_pos)
        else:
            self._set_status("✕  FAILED", C_GOAL)

    def stop_search(self):
        self.running=False
        if self._draw_job:  self.root.after_cancel(self._draw_job)
        if self._agent_job: self.root.after_cancel(self._agent_job)
        self._start_btn.set_enabled(True) if hasattr(self,'_start_btn') else None
        self._stop_btn.set_enabled(False)  if hasattr(self,'_stop_btn')  else None
        self._set_status("STOPPED", TEXT_DIM) if hasattr(self,'status_var') else None

    def reset_search(self):
        self.stop_search()
        self._reset_sets(); self.path=[]; self.visited=[]
        self.agent_pos=None; self._replan_count=0
        self.nodes_var.set("—"); self.cost_var.set("—")
        self.time_var.set("—"); self.replan_var.set("0")
        self._set_status("READY", ACCENT)
        self.draw_grid()

    def _set_status(self, text, color):
        self.status_var.set(text)
        if hasattr(self, '_status_lbl'):
            self._status_lbl.config(fg=color)
        if hasattr(self, '_status_pill'):
            self._status_pill.config(bg=color if color not in (TEXT_DIM,) else BORDER)


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(980, 640)
    app = PathfindingApp(root)
    root.mainloop()