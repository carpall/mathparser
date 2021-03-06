class Node:
  def __init__(self, kind, pos):
    self.kind, self.pos = kind, pos
  
  def __repr__(self):
    return self.__str__()

class BinNode(Node):
  def __init__(self, op, left, right, pos):
    super().__init__('bin', pos)
    self.op, self.left, self.right = op, left, right
  
  def __str__(self):
    return f'<{self.kind} @ {self.left} | {self.op} | {self.right}>'

class UnNode(Node):
  def __init__(self, op, expr, pos):
    super().__init__('un', pos)
    self.op, self.expr = op, expr
  
  def __str__(self):
    return f'<{self.kind} @ {self.op} | {self.expr}>'

class NumberNode(Node):
  def __init__(self, value, pos):
    super().__init__('num', pos)
    self.value = value
  
  def __str__(self):
    return f'<{self.kind} @ {self.value}>'

class VariableNode(Node):
  def __init__(self, name, pos):
    super().__init__('var', pos)
    self.name = name
  
  def __str__(self):
    return f'<{self.kind} @ {self.name}>'

class CallNode(Node):
  def __init__(self, name, args, pos):
    super().__init__('call', pos)
    self.name, self.args = name, args

  def __str__(self):
    return f'<{self.kind} @ {self.name} | {self.args}>'

class EquationNode(Node):
  def __init__(self, op, left, right, pos):
    super().__init__('eq', pos)
    self.op, self.left, self.right = op, left, right

  def __str__(self):
    return f'<{self.kind} @ {self.op} | {self.left} | {self.right}>'

class AssignNode(Node):
  def __init__(self, name, expr, pos):
    super().__init__('assign', pos)
    self.name, self.expr = name, expr

  def __str__(self):
    return f'<{self.kind} @ {self.op} | {self.left} | {self.right}>'