class EvaluatorException(Exception):
  def __init__(self, msg, pos):
    self.msg, self.pos = msg, pos

class CustomFnCaller:
  def __init__(self, args, expr, evaluator_ref):
    self.args, self.expr, self.evaluator_ref = args, expr, evaluator_ref
  
  def call(self, evaluated_args, pos):
    if len(self.args) != len(evaluated_args):
      raise TypeError('wrong number of arguments')
    
    old_symbols = clone_dictionary(self.evaluator_ref.symbols)
    
    for i, arg in enumerate(self.args):
      self.evaluator_ref.symbols[arg] = evaluated_args[i]

    try:
      r = self.evaluator_ref.eval_node(self.expr)
      self.evaluator_ref.symbols = old_symbols

      return r
    except EvaluatorException as e:
      raise EvaluatorException(f'inside function: {e.msg}', pos)

def fib(n):
  a, b = 0, 1

  for _ in range(n):
    a, b = b, a + b
  
  return a

def clone_dictionary(dict):
  return {k: v for k, v in dict.items()}