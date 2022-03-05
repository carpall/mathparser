class EvaluatorException(Exception):
  def __init__(self, msg, pos):
    self.msg, self.pos = msg, pos