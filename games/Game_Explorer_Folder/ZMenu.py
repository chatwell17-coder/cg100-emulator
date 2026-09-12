# Starfall Quest menus for stock fx-CG100 Python.
from casioplot import getkey
from ZCodes import ALPHABET, make_code, read_code
import ZArt as art

UP = 14
LEFT = 23
OK = 24
RIGHT = 25
DOWN = 34
EXE = 95
ZERO = 91

def wait_key():
  key = 0
  while not key:
    key = getkey()
  while getkey():
    pass
  return key

def message(title, text):
  art.panel(title, [text], "Press any key")
  wait_key()

def choose(title, items, footer, zero=False):
  choice = 0
  while True:
    lines = []
    for n in range(len(items)):
      lines.append(("> " if n == choice else "  ") + items[n])
    art.panel(title, lines, footer)
    key = wait_key()
    if key == UP:
      choice = (choice - 1) % len(items)
    elif key == DOWN:
      choice = (choice + 1) % len(items)
    elif key == EXE or key == OK:
      return choice
    elif key == ZERO and zero:
      return 0

def code_editor(fresh):
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
      state = read_code("".join(chars), fresh)
      if state is not None:
        return state
      message("INVALID CODE", "Check every character and try again.")

def title_menu(fresh):
  while True:
    choice = choose("STARFALL QUEST", ("NEW QUEST", "LOAD CODE",
                    "HOW TO PLAY", "EXIT GAME"),
                    "Arrows choose   EXE select")
    if choice == 0:
      return fresh()
    if choice == 1:
      state = code_editor(fresh)
      if state is not None:
        return state
    elif choice == 2:
      art.panel("HOW TO PLAY", ["Arrows: move and face",
                "EXE: strike   OK: use/talk",
                "0: pause and save"], "Defeat foes, find relics, explore!")
      wait_key()
    else:
      return None

def item_text(state):
  names = "Sunblade"
  if state["gear"] & 1:
    names += ", Moon Key"
  if state["gear"] & 2:
    names += ", Star Lens"
  if state["gear"] & 4:
    names += ", Dawn Relic"
  return names

def quest_text(state):
  if state["gear"] & 4:
    return "Quest complete! Starfall is safe."
  if not (state["gear"] & 1):
    return "Clear Briar Field east of Haven."
  if state["room"] < 3:
    return "Use the Moon Key at the northern gate."
  if not (state["cleared"] & 8):
    return "Defeat every foe in Echo Hall."
  if not (state["gear"] & 2):
    return "Search the Astral Vault for the Lens."
  return "Climb north and defeat the Warden."

def pause(state):
  while True:
    choice = choose("PAUSED", ("RESUME", "QUEST", "SHOW SAVE CODE",
                    "ITEMS", "CONTROLS", "QUIT TO TITLE"),
                    "UP/DOWN choose   EXE select", True)
    if choice == 0:
      return False
    if choice == 1:
      message("CURRENT QUEST", quest_text(state))
    elif choice == 2:
      message("SAVE CODE", make_code(state))
    elif choice == 3:
      message("ITEMS", item_text(state))
    elif choice == 4:
      art.panel("CONTROLS", ["Arrows move   EXE strikes",
                "OK uses tonic or talks",
                "0 opens this menu"], "Battles advance one turn per action.")
      wait_key()
    else:
      return True
