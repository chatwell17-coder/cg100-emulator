# Starfall Quest - turn-based adventure for stock fx-CG100 Python.
from casioplot import getkey
from ZMaps import FOES, LINKS, SOLID, tile, room_ok
from ZCodes import ALPHABET, make_code, read_code
import ZArt as art

UP = 14
LEFT = 23
OK = 24
RIGHT = 25
DOWN = 34
EXE = 95
ZERO = 91
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
GEAR_KEY = 1
GEAR_LENS = 2
GEAR_RELIC = 4

def wait_key():
  key = 0
  while not key:
    key = getkey()
  while getkey():
    pass
  return key

def new_game():
  return {"room": 0, "x": 3, "y": 5, "face": 1,
          "maxhp": 3, "hp": 3, "rupees": 0, "gear": 0,
          "potions": 1, "cleared": 0, "turn": 0, "full": 0}

def spawn(room, cleared):
  if cleared & (1 << room):
    return []
  hp = {"S": 1, "B": 1, "K": 2, "W": 6}
  answer = []
  for data in FOES[room]:
    answer.append([data[0], data[1], data[2], hp[data[2]]])
  return answer

def message(title, text):
  art.panel(title, [text], "Press any key")
  wait_key()

def code_editor():
  chars = ["2"] * 10
  pos = 0
  while True:
    art.panel("LOAD SAVE CODE", ["".join(chars), " " * pos + "^",
              "UP/DOWN change  LEFT/RIGHT move"], "EXE load   0 cancel")
    key = wait_key()
    if key == UP:
      at = ALPHABET.find(chars[pos])
      chars[pos] = ALPHABET[(at + 1) % 32]
    elif key == DOWN:
      at = ALPHABET.find(chars[pos])
      chars[pos] = ALPHABET[(at - 1) % 32]
    elif key == LEFT:
      pos = (pos - 1) % 10
    elif key == RIGHT or key == OK:
      pos = (pos + 1) % 10
    elif key == ZERO:
      return None
    elif key == EXE:
      state = read_code("".join(chars), new_game)
      if state is not None:
        return state
      message("INVALID CODE", "Check every character and try again.")

def title_menu():
  choice = 0
  items = ("NEW QUEST", "LOAD CODE", "HOW TO PLAY")
  while True:
    lines = []
    for n in range(3):
      lines.append(("> " if n == choice else "  ") + items[n])
    art.panel("STARFALL QUEST", lines, "Arrows choose   EXE select")
    key = wait_key()
    if key == UP:
      choice = (choice - 1) % 3
    elif key == DOWN:
      choice = (choice + 1) % 3
    elif key == EXE or key == OK:
      if choice == 0:
        return new_game()
      if choice == 1:
        state = code_editor()
        if state is not None:
          return state
      else:
        message("CONTROLS", "Arrows move, EXE strike, OK tonic, 0 pause.")

def clear_reward(state):
  room = state["room"]
  state["cleared"] |= 1 << room
  if room == 1:
    state["gear"] |= GEAR_KEY
    message("FIELD CLEARED", "You found the Moon Key!")
  elif room == 3:
    state["maxhp"] += 1
    state["hp"] = state["maxhp"]
    message("HALL CLEARED", "A Heart Seed raises your health!")
  elif room == 4:
    state["gear"] |= GEAR_LENS
    state["potions"] = min(3, state["potions"] + 1)
    message("VAULT CLEARED", "Star Lens found. Your reach grows!")
  elif room == 5:
    state["gear"] |= GEAR_RELIC
    message("QUEST COMPLETE", "The Warden falls. Starfall is safe!")
  state["full"] = 1

def foe_at(foes, x, y):
  for foe in foes:
    if foe[0] == x and foe[1] == y:
      return foe
  return None

def sword(state, foes):
  dx, dy = DIRS[state["face"]]
  reach = 2 if state["gear"] & GEAR_LENS else 1
  for step in range(1, reach + 1):
    x = state["x"] + dx * step
    y = state["y"] + dy * step
    if tile(state["room"], x, y) in SOLID:
      break
    foe = foe_at(foes, x, y)
    if foe is not None:
      foe[3] -= 1
      if foe[3] <= 0:
        state["rupees"] = min(99, state["rupees"] + (15 if foe[2] == "W" else 3))
        foes.remove(foe)
        if len(foes) == 0 and len(FOES[state["room"]]) > 0:
          clear_reward(state)
      return True
  return True

def can_enter(state, direction):
  room = state["room"]
  if room == 2 and direction == 0 and not (state["gear"] & GEAR_KEY):
    message("SEALED GATE", "The violet arch needs a key.")
    state["full"] = 1
    return False
  if room == 3 and direction == 0 and not (state["cleared"] & (1 << 3)):
    message("DOOR BARRED", "Defeat every foe in this hall.")
    state["full"] = 1
    return False
  if room == 4 and direction == 0 and not (state["gear"] & GEAR_LENS):
    message("DARK SEAL", "The Star Lens can open this way.")
    state["full"] = 1
    return False
  return True

def move_player(state, foes, direction):
  state["face"] = direction
  dx, dy = DIRS[direction]
  nx, ny = state["x"] + dx, state["y"] + dy
  if nx < 0 or nx > 23 or ny < 0 or ny > 9:
    link = LINKS[state["room"]][direction]
    if link < 0 or not can_enter(state, direction):
      return foes, False, False
    state["room"] = link
    state["x"] = 1 if direction == 1 else (22 if direction == 3 else nx)
    state["y"] = 1 if direction == 2 else (8 if direction == 0 else ny)
    return spawn(link, state["cleared"]), True, True
  if tile(state["room"], nx, ny) in SOLID or foe_at(foes, nx, ny) is not None:
    return foes, False, False
  state["x"], state["y"] = nx, ny
  return foes, True, False

def enemy_turn(state, foes):
  state["turn"] += 1
  old = []
  occupied = []
  for foe in foes:
    old.append((foe[0], foe[1]))
    occupied.append((foe[0], foe[1]))
  hits = 0
  for foe in foes:
    dist = abs(foe[0] - state["x"]) + abs(foe[1] - state["y"])
    if dist == 1:
      hits += 1
      continue
    if foe[2] == "S" and state["turn"] % 2:
      continue
    dx = 0
    dy = 0
    if (state["turn"] + foe[0]) % 2 and foe[0] != state["x"]:
      dx = 1 if state["x"] > foe[0] else -1
    elif foe[1] != state["y"]:
      dy = 1 if state["y"] > foe[1] else -1
    elif foe[0] != state["x"]:
      dx = 1 if state["x"] > foe[0] else -1
    nx, ny = foe[0] + dx, foe[1] + dy
    if tile(state["room"], nx, ny) not in SOLID and (nx, ny) not in occupied:
      occupied.remove((foe[0], foe[1]))
      foe[0], foe[1] = nx, ny
      occupied.append((nx, ny))
  if hits:
    state["hp"] -= hits
  return old

def pause(state):
  choice = 0
  while True:
    items = ("RESUME", "SHOW SAVE CODE", "ITEMS", "QUIT TO TITLE")
    lines = []
    for n in range(4):
      lines.append(("> " if n == choice else "  ") + items[n])
    art.panel("PAUSED", lines, "UP/DOWN choose   EXE select")
    key = wait_key()
    if key == UP:
      choice = (choice - 1) % 4
    elif key == DOWN:
      choice = (choice + 1) % 4
    elif key == ZERO and choice != 3:
      return False
    elif key == EXE or key == OK:
      if choice == 0:
        return False
      if choice == 1:
        message("SAVE CODE", make_code(state))
      elif choice == 2:
        names = "Sword"
        if state["gear"] & GEAR_KEY:
          names += ", Moon Key"
        if state["gear"] & GEAR_LENS:
          names += ", Star Lens"
        if state["gear"] & GEAR_RELIC:
          names += ", Dawn Relic"
        message("ITEMS", names)
      else:
        return True

def play(state):
  foes = spawn(state["room"], state["cleared"])
  art.room(state, foes)
  while True:
    key = wait_key()
    cells = [(state["x"], state["y"])]
    for foe in foes:
      cells.append((foe[0], foe[1]))
    acted = False
    changed_room = False
    if key in (UP, RIGHT, DOWN, LEFT):
      direction = (UP, RIGHT, DOWN, LEFT).index(key)
      foes, acted, changed_room = move_player(state, foes, direction)
    elif key == EXE:
      acted = sword(state, foes)
    elif key == OK and state["potions"] > 0 and state["hp"] < state["maxhp"]:
      state["potions"] -= 1
      state["hp"] = min(state["maxhp"], state["hp"] + 2)
      acted = True
    elif key == ZERO:
      if pause(state):
        return
      art.room(state, foes)
      continue
    if changed_room:
      art.room(state, foes)
      continue
    if acted:
      cells += enemy_turn(state, foes)
      if state["hp"] <= 0:
        message("YOU FELL", "You wake in Haven with half your rupees.")
        state["room"], state["x"], state["y"] = 0, 3, 5
        state["hp"] = state["maxhp"]
        state["rupees"] //= 2
        foes = spawn(0, state["cleared"])
        art.room(state, foes)
      elif state["full"]:
        state["full"] = 0
        art.room(state, foes)
      else:
        cells.append((state["x"], state["y"]))
        art.refresh_cells(state, foes, cells)
    elif state["full"]:
      state["full"] = 0
      art.room(state, foes)

def main():
  if not room_ok():
    message("MAP ERROR", "A room row has the wrong size.")
    return
  while True:
    play(title_menu())

main()
