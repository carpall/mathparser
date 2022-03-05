from xtoken import *

TOKENS = ['+', '-', '*', '/', '(', ')', 'num', 'eof', 'bad']
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
    
    if self.cur().isdigit():
      token = self.collect_number()
    else:
      cur = self.cur()
      kind = cur if cur in TOKENS else 'bad'
      token = self.collect_group_of_bad_characters() if kind == 'bad' else Token(kind, cur, self.cur_pos())

    self.index += 1
    return token

  def collect_group_of_bad_characters(self):
    start = self.cur_pos()
    old_index = self.index

    if not self.cur().isalnum():
      return Token('bad', self.cur(), start)

    while not self.reached_eof() and self.cur().isalnum():
      self.index += 1

    self.index -= 1
    return Token('bad', self.expr[old_index:self.index], range(start.start, self.cur_pos().stop))

  def collect_number(self):
    start = self.cur_pos()
    number = ''
    reached_dot = False

    while not self.reached_eof() and ((cur := self.cur()).isdigit() or cur == '.'):
      if cur == '.':
        if reached_dot:
          break

        reached_dot = True

      number += cur
      self.index += 1

    self.index -= 1
    return Token('num', number, range(start.start, self.cur_pos().stop))

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