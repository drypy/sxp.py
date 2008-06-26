symbols = {}

def intern(name):
  try:
    return symbols[name]
  except KeyError:
    symbol = Symbol(name)
    symbols[name] = symbol
    return symbol

class Symbol(object):
  def __init__(self, name):
    self.name = name
  def __repr__(self):
    return self.name
