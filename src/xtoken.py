class Token:
  def __init__(self, kind, value, pos):
    self.kind = kind
    self.value = value
    self.pos = pos
  
  def __str__(self):
    return f'<token @ {self.kind.__repr__()} | {self.value.__repr__()}>'