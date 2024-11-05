import os
from decimal import *

class Interval:
  def __init__(self, s, e):
    self.s = s
    self.e = e
    self.r = e - s
  def multiply(self, other):
    news = self.s + (self.r * other.s)
    newe = self.s + (self.r * other.e)
    return Interval(news, newe)
  def __contains__(self, point):
    return (self.s <= point) and (self.e >= point)
  def __str__(self):
    return "[{x}, {y})".format(x=self.s, y=self.e)

class Code:
  def __init__(self, costs):
    self.costs = costs

    total = 0
    for letter in costs:
      total = total + costs[letter]

    start = 0
    self.intervals = {}
    for letter in costs:
      end = start + costs[letter]
      self.intervals[letter] = Interval(Decimal(start) / Decimal(total), Decimal(end) / Decimal(total))
      start = end

  def encode(self, target, scale):
    scale = scale
    before = (target - 1) / scale
    after = (target + 1) / scale
    target = target / scale
    (result, current) = self.find(target)
    while before in current or after in current:
      (letter, current) = self.fit(current, target)
      result += letter
    return result

  def decode(self, encoding, scale):
    current = None
    for letter in encoding:
      if current:
        current = current.multiply(self.intervals[letter])
      else:
        current = self.intervals[letter]

    return Interval(current.s * scale, current.e * scale)

  def find(self, target):
    for letter in self.intervals:
      interval = self.intervals[letter]
      if target in interval:
        return (letter, interval)

    return None

  def fit(self, current, target):
    found = None
    result = None
    for letter in self.intervals:
      interval = self.intervals[letter]
      option = current.multiply(interval)
      if target in option:
        if result:
          if option.r < result.r:
            result = option
            found = letter
        else:
          result = option
          found = letter

    if result:
      return (found, result)
    else:
      return None

  def print(self, letters):
    count = 0
    for letter in letters:
      print(letter, end="")
      count += 1
      if count % 8 == 0:
        print(' ', end="")
    print(' ')

  def totalCost(self, letters):
    result = 0
    for letter in letters:
      if letter == ' ':
        result += 4
      else:
        result += self.costs[letter]

    return result

if __name__ == '__main__':
  morseCosts = {
    'A': 8,
    'B': 12,
    'C': 14,
    'D': 10,
    'E': 4,
    'F': 12,
    'G': 11,
    'H': 10,
    'I': 6,
    'J': 13,
    'K': 10,
    'L': 12,
    'M': 9,
    'N': 7,
    'O': 12,
    'P': 14,
    'Q': 15,
    'R': 8,
    'S': 8,
    'T': 6,
    'U': 8,
    'V': 10,
    'W': 11,
    'X': 14,
    'Y': 15,
    'Z': 13,
  }

  messageSize = 256 # in bytes
  context = getcontext()
  context.prec = messageSize*8
  code = Code(morseCosts)

  random_bytes = os.urandom(messageSize)
  target = 0
  for byte in random_bytes:
    target = (target << 8) + byte
  target = Decimal(target)
  scale = Decimal(2 ** (messageSize * 8))
  encoding = code.encode(target, scale)
  code.print(encoding)
  cost = code.totalCost(encoding)
  print("{x} dits, {y} minutes at 15 wpm".format(x=cost, y=round(cost/750)))
  decoded = code.decode(encoding, scale)
  print(target.to_integral_exact() == decoded.s.to_integral_exact())