from sys       import stderr
from evaluator import *
from utilities import *

def print_error(error):
  for _ in range(error.pos.start + 2): print(file=stderr, end=' ')

  for _ in error.pos: print(file=stderr, end='-')

  print(f' {error.msg}', file=stderr)

try:
  while True:
    if (expr := input('> ')) == '': continue

    try:
      evaluated = Evaluator(expr).evaluate()
      result = str(evaluated).replace('.0', '')

      print(result)
    except EvaluatorException as e:
      print_error(e)
except KeyboardInterrupt:
  print('')