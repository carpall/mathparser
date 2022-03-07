from operator   import add, sub, mul, truediv as div
from types      import LambdaType
from utilities  import *
from xparser    import *
from math       import sqrt, log, log10, sin, cos, tan, nan, inf, tau

PI = 3.14159265359
E = 2.718281828459045
PHI = 1.61803399

BUILTINS = {
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
  'pi':    PI,
  'e':     E,
  'phi':   PHI,
  'nan':   nan,
  'inf':   inf,
  'tau':   tau
}

class Evaluator:
  def __init__(self):
    self.symbols = clone_dictionary(BUILTINS)

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

  def check_fn_decl(self, args):
    return all([isinstance(arg, VariableNode) for arg in args])

  def eval_assign(self, node):
    kind = node.name.kind
    name = node.name.name

    if kind == 'var':
      self.symbols[name] = self.eval_node(node.expr)
    elif kind == 'call' and self.check_fn_decl(node.name.args):
      self.symbols[name] = CustomFnCaller([arg.name for arg in node.name.args], node.expr, self)
    else:
      raise EvaluatorException('expression cannot be assigned', node.pos)

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

  def get_symbol(self, name, pos):
    try:
      return self.symbols[name]
    except KeyError:
      raise EvaluatorException('unknown symbol', pos)

  def eval_var(self, node):
    s = self.get_symbol(node.name, node.pos)

    if isinstance(s, CustomFnCaller) or isinstance(s, LambdaType):
      raise EvaluatorException('function need to be called', node.pos)
    
    return s

  def eval_call(self, node):
    try:
      s = self.get_symbol(node.name, node.pos)
      args = [self.eval_node(arg) for arg in node.args]

      if isinstance(s, CustomFnCaller):
        return s.call(args, node.pos)
        
      return s(*args)
    except TypeError:
      raise EvaluatorException('bad function construction', node.pos)

  def eval_node(self, node):
    return getattr(Evaluator, f'eval_{node.kind}')(self, node)

  def evaluate(self, expr):
    self.parser = Parser(expr)
    return self.eval_node(self.parser.parse())