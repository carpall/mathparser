from node      import *
from xlexer    import *
from utilities import *

class Parser:
  def __init__(self, expr):
    self.lexer = Lexer(expr)
  
  def match_token(self, token):
    if isinstance(token, str):
      return self.lexer.head.kind == token
    
    for t in token:
      if self.match_token(t):
        return True

    return False

  def expect_pattern(self, terms_collector_function, operators):
    left = terms_collector_function(self)
    
    while self.match_token(operators):
      op = self.lexer.consume()
      right = terms_collector_function(self)
      left = BinNode(op, left, right, range(left.pos.start, right.pos.stop))

    return left

  def expect_token(self, token):
    if self.match_token(token):
      return self.lexer.consume()
      
    raise EvaluatorException(f"expect '{token}'", self.lexer.head.pos)

  def collect_parentesis(self):
    start_pos = self.lexer.back.pos.start
    expr = self.expect_expression()
    end_pos = self.expect_token(')').pos.stop

    expr.pos = range(start_pos, end_pos)

    return expr

  def colect_unary(self, op):
    expr = self.expect_term()

    return UnNode(op, expr, range(op.pos.start, expr.pos.stop))

  def parse_call_args(self):
    args = []

    while not self.match_token(')'):
      if len(args) > 0:
        self.expect_token(',')

      args.append(self.expect_expression())

    return args, self.lexer.consume().pos

  def parse_call(self, token):
    # eating '('
    self.lexer.consume()

    args, rpar_pos = self.parse_call_args()
    name = token.value
    pos = range(token.pos.start, rpar_pos.stop)

    return Call(name, args, pos)

  def parse_call_or_var(self, token):
    return self.parse_call(token) if self.match_token('(') else Variable(token.value, token.pos)

  def expect_term(self):
    cur = self.lexer.consume()

    match cur.kind:
      case 'id': return self.parse_call_or_var(cur)
      case 'num': return Number(float(cur.value), cur.pos)
      case '(': return self.collect_parentesis()
      case '+' | '-': return self.colect_unary(cur)
      case _: raise EvaluatorException('unexpected token', cur.pos)
  
  def expect_factor(self):
    return self.expect_pattern(Parser.expect_term, ['*', '/'])

  def expect_expression(self):
    return self.expect_pattern(Parser.expect_factor, ['+', '-'])

  def parse(self):
    expr = self.expect_expression()
    self.expect_token('eof')

    return expr