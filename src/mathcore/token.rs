use crate::mathcore::Position;

#[derive(Clone, PartialEq)]
pub enum TokenKind {
  Number,
  Plus,
  Minus,
  Star,
  Slash,
  LeftPar,
  RightPar,
  Bad,
  Eof
}

#[derive(Clone)]
pub struct Token {
  kind: TokenKind,
  value: String,
  position: Position
}

impl Token {
  pub fn from(kind: TokenKind, value: String, position: Position) -> Self {
    Self {
      kind: kind,
      value: value,
      position: position
    }
  }

  pub fn get_kind(&self) -> TokenKind { self.kind.clone() }
  
  pub fn get_value(&self) -> String { self.value.clone() }

  pub fn get_position(&self) -> Position { self.position.clone() }
}