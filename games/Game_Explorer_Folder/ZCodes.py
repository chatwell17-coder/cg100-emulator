# Compact, checked save codes. No file writes are used.
from ZMaps import SOLID, tile

ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

def make_code(s):
  values = (s["room"], s["x"], s["y"], s["maxhp"] - 3,
            s["hp"], s["rupees"], s["gear"], s["potions"],
            s["cleared"])
  bases = (6, 24, 10, 7, 10, 100, 8, 4, 64)
  value = 1
  for n in range(len(values)):
    value = value * bases[n] + values[n]
  raw = ""
  work = value
  for n in range(8):
    raw = ALPHABET[work % 32] + raw
    work //= 32
  check = (value * 17 + 137) % 1024
  return raw + ALPHABET[check // 32] + ALPHABET[check % 32]

def read_code(code, fresh):
  if len(code) != 10:
    return None
  nums = []
  for char in code:
    pos = ALPHABET.find(char)
    if pos < 0:
      return None
    nums.append(pos)
  value = 0
  for n in range(8):
    value = value * 32 + nums[n]
  if (value * 17 + 137) % 1024 != nums[8] * 32 + nums[9]:
    return None
  work = value
  bases = (6, 24, 10, 7, 10, 100, 8, 4, 64)
  fields = [0] * 9
  for n in range(8, -1, -1):
    fields[n] = work % bases[n]
    work //= bases[n]
  if work != 1:
    return None
  s = fresh()
  s["room"], s["x"], s["y"] = fields[0], fields[1], fields[2]
  s["maxhp"] = fields[3] + 3
  s["hp"], s["rupees"] = fields[4], fields[5]
  s["gear"], s["potions"], s["cleared"] = fields[6], fields[7], fields[8]
  if s["hp"] < 1 or s["hp"] > s["maxhp"]:
    return None
  if tile(s["room"], s["x"], s["y"]) in SOLID:
    return None
  return s
