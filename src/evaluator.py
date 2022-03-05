from operator   import add, sub, mul, truediv as div
from utilities  import EvaluatorException
from xparser    import *

class Evaluator:
  def __init__(self, expr):
    self.parser = Parser(expr)

  def eval_bin(self, node):
    op_call = {
      '+': add,
      '-': sub,
      '*': mul,
      '/': div,
    }[node.op.kind]

    try:
      return op_call(self.eval_node(node.left), self.eval_node(node.right))
    except ZeroDivisionError:
      raise EvaluatorException('dividing by zero', range(node.op.pos.start, node.right.pos.stop))

  def eval_un(self, node):
    t = self.eval_node(node.expr)

    return t if node.op.kind == '+' else -t

  def eval_num(self, node):
    return node.value

  def eval_node(self, node):
    return getattr(Evaluator, f'eval_{node.kind}')(self, node)

  def evaluate(self):
    return self.eval_node(self.parser.parse())