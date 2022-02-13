use crate::mathcore;
use mathcore::Token;
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
    let mut lexer = Self {
      expression: expression,
      index: 0,
      back: Token::Bad(0..0),
      head: Token::Bad(0..0)
    };

    lexer.consume();

    lexer
  }

  #[allow(dead_code)]
  pub fn back(self) -> Token { self.back }

  pub fn head(self) -> Token { self.head }

  pub fn consume(&mut self) -> Token {
    self.back = self.head.clone();
    self.head = self.next();

    self.back.clone()
  }

  fn next(&mut self) -> Token {
    self.eat_whitespace();

    if self.reached_eof() { return Token::Eof(self.get_eof_position()); }

    let token =
      if self.cur().is_ascii_digit() {
        self.collect_number()
      } else {
        match self.cur() {
          '+' => Token::Plus(self.cur_pos()),
          '-' => Token::Minus(self.cur_pos()),
          '*' => Token::Star(self.cur_pos()),
          '/' => Token::Slash(self.cur_pos()),
          '(' => Token::LeftPar(self.cur_pos()),
          ')' => Token::RightPar(self.cur_pos()),
          _ => self.collect_group_of_bad_characters()
        }
      };

    // dbg!(token.clone());
    self.index += 1;
    token
  }

  fn collect_group_of_bad_characters(&mut self) -> Token {
    let start = self.cur_pos();

    if !self.cur().is_alphanumeric() { return Token::Bad(start); }

    while !self.reached_eof() && self.cur().is_alphanumeric() {
      self.index += 1;
    }

    self.index -= 1;
    Token::Bad(start.start..self.cur_pos().end)
  }

  fn collect_number(&mut self) -> Token {
    let start = self.cur_pos();
    let mut number = String::new();

    while !self.reached_eof() && self.cur().is_ascii_digit() {
      number.push(self.cur());
      self.index += 1;
    }

    self.index -= 1;
    Token::Number(number.parse::<f64>().unwrap(), start.start..self.cur_pos().end)
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