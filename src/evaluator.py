from operator   import add, sub, mul, truediv as div
from utilities  import EvaluatorException
from xparser    import *
from math       import sqrt, log, log10, sin, cos, tan, nan, inf, tau

def fib(n):
  a, b = 0, 1

  for _ in range(n):
    a, b = b, a + b
  
  return a

PI = 3.14159265359
E = 2.718281828459045
PHI = 1.61803399

BUILTIN_FN = {
  'sqrt':  lambda x: sqrt(x),
  'root':  lambda x, y: y ** (1 / x),
  'log':   lambda x, y: log(y, x),
  'log10': lambda x: log10(x),
  'ln':    lambda x: log(x, E),
  'sin':   lambda x: sin(x),
  'cos':   lambda x: cos(x),
  'tan':   lambda x: tan(x),
  'fib':   lambda x: fib(int(x)),
  'min':   lambda x, y: min(x, y),
  'max':   lambda x, y: max(x, y),
}

BUILTIN_VAR = {
  'pi':  PI,
  'e':   E,
  'phi': PHI,
  'nan': nan,
  'inf': inf,
  'tau': tau
}

class Evaluator:
  def __init__(self):
    self.vars = {}

  def eval_bin(self, node):
    op_call = {
      '+': add,
      '-': sub,
      '*': mul,
      '/': div,
      '^': pow,
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

  def eval_assign(self, node):
    self.vars[node.name] = self.eval_node(node.expr)

  def eval_eq(self, node):
    l = self.eval_node(node.left)
    r = self.eval_node(node.right)

    op = {
      '=':  lambda x, y: x == y,
      '!=': lambda x, y: x != y,
      '<':  lambda x, y: x < y,
      '>':  lambda x, y: x > y,
      '<=': lambda x, y: x <= y,
      '>=': lambda x, y: x >= y,
    }[node.op]

    return 'imp' if not op(l, r) else None

  def eval_var(self, node):
    try:
      return BUILTIN_VAR[node.name]
    except KeyError:
      try:
        return self.vars[node.name]
      except KeyError:
        raise EvaluatorException(f'unknown variable', node.pos)

  def eval_call(self, node):
    try:
      fn = BUILTIN_FN[node.name]
      return fn(*[self.eval_node(arg) for arg in node.args])
    except KeyError:
      raise EvaluatorException('unknown function', node.pos)
    except TypeError:
      raise EvaluatorException('wrong args', node.pos)

  def eval_node(self, node):
    return getattr(Evaluator, f'eval_{node.kind}')(self, node)

  def evaluate(self, expr):
    self.parser = Parser(expr)
    return self.eval_node(self.parser.parse())