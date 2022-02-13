use crate::mathcore::Position;

#[derive(Debug, Clone)]
pub enum Token {
  Number(f64, Position),
  Plus(Position),
  Minus(Position),
  Star(Position),
  Slash(Position),
  LeftPar(Position),
  RightPar(Position),
  Bad(Position),
  Eof(Position)
}

impl Token {
  pub fn get_position(self) -> Position {
    match self {
      Token::Number(_, position) => position,
      Token::Plus(position) => position,
      Token::Minus(position) => position,
      Token::Star(position) => position,
      Token::Slash(position) => position,
      Token::LeftPar(position) => position,
      Token::RightPar(position) => position,
      Token::Bad(position) => position,
      Token::Eof(position) => position,
    }
  }

  pub fn cmp_tag(self, right: Token) -> bool {
    std::mem::discriminant(&self) == std::mem::discriminant(&right)
  }
}