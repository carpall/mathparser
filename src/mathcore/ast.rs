use crate::mathcore;
use mathcore::Position;
use mathcore::Token;

#[derive(Clone)]
pub enum BinaryOperator {
  Plus(Position),
  Minus(Position),
  Star(Position),
  Slash(Position)
}

#[derive(Clone)]
pub enum UnaryOperator {
  Plus(Position),
  Minus(Position)
}

#[derive(Clone)]
pub enum Node {
  Number(f64, Position),
  BinaryOperation(BinaryOperator, Box<Node>, Box<Node>),
  UnaryOperation(UnaryOperator, Box<Node>)
}

impl BinaryOperator {
  pub fn from_token(token: Token) -> Self {
    match token {
      Token::Plus(position) => Self::Plus(position),
      Token::Minus(position) => Self::Minus(position),
      Token::Star(position) => Self::Star(position),
      Token::Slash(position) => Self::Slash(position),
      _ => unreachable!()
    }
  }

  #[allow(dead_code)] 
  pub fn get_position(self) -> Position {
    match self {
      BinaryOperator::Plus(position) => position,
      BinaryOperator::Minus(position) => position,
      BinaryOperator::Star(position) => position,
      BinaryOperator::Slash(position) => position,
    }
  }
}

impl UnaryOperator {
  pub fn from_token(token: Token) -> Self {
    match token {
      Token::Plus(position) => Self::Plus(position),
      Token::Minus(position) => Self::Minus(position),
      _ => unreachable!()
    }
  }

  pub fn get_position(self) -> Position {
    match self {
      UnaryOperator::Plus(position) => position,
      UnaryOperator::Minus(position) => position,
    }
  }
}

impl Node {
  pub fn get_position(self) -> Position {
    match self {
      Node::Number(_, position) => position,
      Node::BinaryOperation(_, left, right) => left.get_position().start..right.get_position().end,
      Node::UnaryOperation(op, node) => op.get_position().start..node.get_position().end
    }
  }
}