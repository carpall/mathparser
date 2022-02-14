use crate::mathcore;
use mathcore::Token;
use mathcore::TokenKind;
use mathcore::Position;

#[derive(Clone)]
pub struct Lexer {
  expression: String,
  index: usize,
  back: Token,
  head: Token
}

impl Lexer {
  pub fn from(expression: String) -> Self {
    let default = Token::from(TokenKind::Bad, String::new(), 0..0);

    let mut lexer = Self {
      expression: expression,
      index: 0,
      back: default.clone(),
      head: default
    };

    lexer.consume();
    lexer
  }

  #[allow(dead_code)]
  pub fn back(&self) -> Token { self.back.clone() }

  pub fn head(&self) -> Token { self.head.clone() }

  pub fn consume(&mut self) -> Token {
    self.back = self.head.clone();
    self.head = self.next();

    self.back.clone()
  }

  fn next(&mut self) -> Token {
    self.eat_whitespace();

    if self.reached_eof() { return Token::from(TokenKind::Eof, String::new(), self.get_eof_position()); }

    let token =
      if self.cur().is_ascii_digit() {
        self.collect_number()
      } else {
        let cur = self.cur();
        let kind = match cur {
          '+' => TokenKind::Plus,
          '-' => TokenKind::Minus,
          '*' => TokenKind::Star,
          '/' => TokenKind::Slash,
          '(' => TokenKind::LeftPar,
          ')' => TokenKind::RightPar,
          _ => TokenKind::Bad
        };

        if kind == TokenKind::Bad {
          self.collect_group_of_bad_characters()
        } else {
          Token::from(kind, String::from(cur), self.cur_pos())
        }
      };

    self.index += 1;
    token
  }

  fn collect_group_of_bad_characters(&mut self) -> Token {
    let start = self.cur_pos();
    let old_index = self.index;

    if !self.cur().is_alphanumeric() { return Token::from(TokenKind::Bad, String::from(self.cur()), start); }

    while !self.reached_eof() && self.cur().is_alphanumeric() {
      self.index += 1;
    }

    self.index -= 1;
    Token::from(TokenKind::Bad, self.expression.chars().skip(old_index).take(self.index).collect(), start.start..self.cur_pos().end)
  }

  fn collect_number(&mut self) -> Token {
    let start = self.cur_pos();
    let mut number = String::new();

    while !self.reached_eof() && self.cur().is_ascii_digit() {
      number.push(self.cur());
      self.index += 1;
    }

    self.index -= 1;
    Token::from(TokenKind::Number, number, start.start..self.cur_pos().end)
  }

  fn cur(&self) -> char { self.expression.chars().nth(self.index).unwrap() }

  fn cur_pos(&self) -> Position { self.index .. self.index + 1 }

  fn reached_eof(&self) -> bool { self.index >= self.expression.len() }

  fn get_eof_position(&self) -> Position {
    let len = self.expression.len();

    if len == 0 { 0..0 } else { len - 1 .. len }
  }

  fn eat_whitespace(&mut self) {
    while !self.reached_eof() && [' ', '\t', '\n'].contains(&self.cur()) {
      self.index += 1;
    }
  }
}