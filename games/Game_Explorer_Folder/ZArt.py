# Small original renderer using only the stock casioplot API.
from casioplot import set_pixel, draw_string, clear_screen, show_screen
from ZMaps import ROOMS, NAMES

WHITE = (255, 255, 255)
INK = (25, 29, 42)
GRASS = (183, 226, 149)
STONE = (104, 110, 126)
WATER = (70, 153, 214)
TREE = (39, 126, 74)
GOLD = (238, 184, 46)
RED = (210, 55, 64)
VIOLET = (116, 71, 155)
CYAN = (62, 199, 199)
TILE = 16
TOP = 29

def fill(x, y, w, h, color):
  for py in range(y, y + h):
    for px in range(x, x + w):
      set_pixel(px, py, color)

def line(x, y, w, color):
  for px in range(x, x + w):
    set_pixel(px, y, color)

def box(x, y, w, h, color):
  line(x, y, w, color)
  line(x, y + h - 1, w, color)
  for py in range(y + 1, y + h - 1):
    set_pixel(x, py, color)
    set_pixel(x + w - 1, py, color)

def heart(x, y, full):
  c = RED if full else STONE
  fill(x + 1, y, 3, 2, c)
  fill(x + 5, y, 3, 2, c)
  fill(x, y + 2, 9, 3, c)
  fill(x + 2, y + 5, 5, 2, c)
  fill(x + 4, y + 7, 1, 1, c)

def hud(state):
  fill(170, 0, 112, 15, WHITE)
  fill(284, 0, 100, 15, WHITE)
  x = 174
  for n in range(state["maxhp"]):
    heart(x + n * 11, 4, n < state["hp"])
  draw_string(286, 2, "$" + str(state["rupees"]), GOLD, "small")
  draw_string(337, 2, "P" + str(state["potions"]), VIOLET, "small")

def draw_tile(room, tx, ty, cleared):
  x = tx * TILE
  y = TOP + ty * TILE
  fill(x, y, TILE, TILE, WHITE)
  ch = ROOMS[room][ty][tx]
  if ch == "." and room < 3 and (tx * 5 + ty * 3) % 13 == 0:
    set_pixel(x + 3, y + 12, GRASS)
    set_pixel(x + 4, y + 10, GRASS)
  if ch == "#":
    fill(x, y, TILE, TILE, STONE)
    box(x + 2, y + 2, 12, 12, INK)
  elif ch == "~":
    for yy in (y + 4, y + 9, y + 14):
      line(x + 1, yy, 12, WATER)
  elif ch == "T":
    fill(x + 3, y + 2, 10, 9, TREE)
    fill(x + 7, y + 10, 3, 6, INK)
  elif ch == "^":
    fill(x + 3, y + 8, 10, 6, STONE)
    line(x + 6, y + 5, 4, STONE)
  elif ch == "G":
    fill(x + 2, y + 1, 12, 14, VIOLET)
    fill(x + 5, y + 4, 6, 11, INK)
  elif ch == "C" and not cleared:
    fill(x + 3, y + 6, 10, 8, GOLD)
    box(x + 3, y + 6, 10, 8, INK)
  elif ch == "V":
    fill(x + 4, y + 3, 8, 10, TREE)
    fill(x + 5, y + 1, 6, 4, VIOLET)
    set_pixel(x + 7, y + 7, WHITE)
    set_pixel(x + 9, y + 7, WHITE)

def actor(tx, ty, color, mark):
  x = tx * TILE
  y = TOP + ty * TILE
  fill(x + 4, y + 3, 8, 10, color)
  box(x + 4, y + 3, 8, 10, INK)
  if mark:
    set_pixel(x + 7, y + 7, WHITE)
    set_pixel(x + 9, y + 7, WHITE)

def draw_player(state):
  actor(state["x"], state["y"], CYAN, True)
  x = state["x"] * TILE + 7
  y = TOP + state["y"] * TILE + 1
  if state["face"] == 0:
    set_pixel(x, y, GOLD)
  elif state["face"] == 1:
    set_pixel(x + 7, y + 7, GOLD)
  elif state["face"] == 2:
    set_pixel(x, y + 13, GOLD)
  else:
    set_pixel(x - 3, y + 7, GOLD)

def draw_foes(foes):
  for foe in foes:
    x = foe[0] * TILE
    y = TOP + foe[1] * TILE
    kind = foe[2]
    if kind == "S":
      fill(x + 3, y + 7, 10, 6, TREE)
      line(x + 5, y + 5, 6, TREE)
      set_pixel(x + 6, y + 9, WHITE)
      set_pixel(x + 10, y + 9, WHITE)
    elif kind == "B":
      fill(x + 6, y + 5, 5, 7, VIOLET)
      line(x + 1, y + 5, 6, VIOLET)
      line(x + 10, y + 5, 5, VIOLET)
      line(x + 3, y + 8, 4, VIOLET)
      line(x + 10, y + 8, 3, VIOLET)
    elif kind == "K":
      actor(foe[0], foe[1], RED, True)
      fill(x + 4, y + 3, 8, 3, STONE)
    else:
      fill(x + 3, y + 2, 10, 12, GOLD)
      box(x + 3, y + 2, 10, 12, VIOLET)
      fill(x + 6, y + 5, 4, 4, INK)
    if foe[3] > 1:
      for n in range(min(6, foe[3])):
        set_pixel(x + 4 + n, y + 1, RED)

def strike(state, reach):
  x = state["x"] * TILE + 8
  y = TOP + state["y"] * TILE + 8
  dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))
  dx, dy = dirs[state["face"]]
  for n in range(6, reach * TILE + 2):
    set_pixel(x + dx * n, y + dy * n, GOLD)
  show_screen()

def room(state, foes):
  clear_screen()
  draw_string(4, 2, NAMES[state["room"]], INK, "small")
  hud(state)
  line(0, 26, 384, INK)
  done = (state["cleared"] & (1 << state["room"])) != 0
  for y in range(10):
    for x in range(24):
      draw_tile(state["room"], x, y, done)
  draw_foes(foes)
  draw_player(state)
  show_screen()

def refresh_cells(state, foes, cells):
  done = (state["cleared"] & (1 << state["room"])) != 0
  used = []
  for pos in cells:
    if pos not in used and 0 <= pos[0] < 24 and 0 <= pos[1] < 10:
      used.append(pos)
      draw_tile(state["room"], pos[0], pos[1], done)
  draw_foes(foes)
  draw_player(state)
  hud(state)
  show_screen()

def panel(title, lines, footer):
  clear_screen()
  box(8, 8, 368, 176, INK)
  draw_string(22, 18, title, VIOLET, "large")
  y = 57
  for text in lines:
    draw_string(24, y, text, INK, "small")
    y += 19
  draw_string(24, 164, footer, STONE, "small")
  show_screen()
