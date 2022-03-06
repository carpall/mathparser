from utilities import EvaluatorException
from xtoken    import *

TOKENS = ['+', '-', '*', '/', '(', ')', ',', 'num', 'id', 'eof', 'bad']
WHITESPACE = [' ', '\t', '\n']

class Lexer:
  def __init__(self, expr):
    default = Token(None, None, None)

    self.expr = expr
    self.head = default
    self.back = default
    self.index = 0

    self.consume()

  def consume(self):
    self.back = self.head
    self.head = self.next()

    return self.back

  def next(self):
    self.eat_whitespace()

    if self.reached_eof():
      return Token('eof', '', self.eof_pos())
    
    cur = self.cur()

    if cur.isdigit():
      token = self.collect_number()
    elif cur.isalpha():
      token = self.collect_identifier()
    else:
      kind = cur if cur in TOKENS else 'bad'
      token = Token(kind, cur, self.cur_pos())

    self.index += 1
    return token

  def collect_pattern(self, kind, pattern_matcher):
    start = self.cur_pos()
    pattern = ''

    while not self.reached_eof() and pattern_matcher(cur := self.cur()):
      pattern += cur
      self.index += 1

    self.index -= 1
    return Token(kind, pattern, range(start.start, self.cur_pos().stop))

  def collect_identifier(self):
    return self.collect_pattern('id', lambda cur: cur.isalnum())

  def collect_number(self):
    first_part = self.collect_pattern('num', lambda cur: cur.isdigit() or cur == '.')

    if first_part.value.count('.') > 1:
      raise EvaluatorException('invalid number', first_part.pos)
    
    return first_part

  def cur(self):
    return self.expr[self.index]

  def cur_pos(self):
    return range(self.index, self.index + 1)

  def reached_eof(self):
    return self.index >= len(self.expr)

  def eof_pos(self):
    l = len(self.expr)

    return range(0, 1) if l == 0 else range(l - 1, l)

  def eat_whitespace(self):
    while not self.reached_eof() and self.cur() in WHITESPACE:
      self.index += 1