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
  fill(170, 0, 214, 25, WHITE)
  x = 174
  for n in range(state["maxhp"]):
    heart(x + n * 11, 4, n < state["hp"])
  draw_string(286, 2, "$" + str(state["rupees"]), GOLD, "small")
  draw_string(337, 2, "P" + str(state["potions"]), VIOLET, "small")
  line(0, 26, 384, INK)

def draw_tile(room, tx, ty, cleared):
  x = tx * TILE
  y = TOP + ty * TILE
  fill(x, y, TILE, TILE, WHITE)
  ch = ROOMS[room][ty][tx]
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
  colors = {"S": TREE, "B": VIOLET, "K": RED, "W": GOLD}
  for foe in foes:
    actor(foe[0], foe[1], colors[foe[2]], foe[2] != "S")

def room(state, foes):
  clear_screen()
  draw_string(4, 2, NAMES[state["room"]], INK, "small")
  hud(state)
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
