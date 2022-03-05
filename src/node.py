class Node:
  def __init__(self, kind, pos):
    self.kind, self.pos = kind, pos

class BinNode(Node):
  def __init__(self, op, left, right, pos):
    super().__init__('bin', pos)
    self.op, self.left, self.right = op, left, right

class UnNode(Node):
  def __init__(self, op, expr, pos):
    super().__init__('un', pos)
    self.op, self.expr = op, expr

class Number(Node):
  def __init__(self, value, pos):
    super().__init__('num', pos)
    self.value = value