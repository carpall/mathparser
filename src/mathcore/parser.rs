use crate::mathcore;
use mathcore::Lexer;
use mathcore::Node;
use mathcore::Token;
use mathcore::BinaryOperator;
use mathcore::UnaryOperator;

#[derive(Clone)]
pub struct Parser {
  lexer: Lexer
}

impl Parser {
  pub fn from(expression: String) -> Self {
    Self {
      lexer: Lexer::from(expression)
    }
  }

  fn match_token(&self, token: Token) -> bool {
    self.lexer.clone().head().cmp_tag(token)
  }

  fn match_tokens(&self, tokens: &[Token]) -> bool {
    for token in tokens {
      if self.match_token(token.clone()) { return true; }
    }

    false
  }

  fn expect_pattern(
    &mut self,
    terms_collector_function: fn(&mut Parser) -> Result<Node, mathcore::Error>,
    operators: &[Token]
  ) -> Result<Node, mathcore::Error> {
    let mut left = terms_collector_function(self)?;
    
    while self.match_tokens(operators) {
      let op = self.lexer.consume();
      let right = terms_collector_function(self)?;

      left = Node::BinaryOperation(
        BinaryOperator::from_token(op),
        Box::from(left),
        Box::from(right)
      );
    }

    Ok(left)
  }

  fn expect_token(&mut self, token: Token) -> Result<(), mathcore::Error> {
    if self.match_token(token) {
      self.lexer.consume();
      Ok(())
    } else {
      Err(mathcore::Error::from("unexpected token".to_string(), self.lexer.clone().head().get_position()))
    }
  }

  fn collect_parentesis(&mut self) -> Result<Node, mathcore::Error> {
    let expression = self.expect_expression()?;
    self.expect_token(Token::RightPar(0..0))?;

    Ok(expression)
  }

  fn colect_unary(&mut self, op: Token) -> Result<Node, mathcore::Error> {
    let expression = self.expect_term()?;

    Ok(Node::UnaryOperation(UnaryOperator::from_token(op), Box::from(expression)))
  }

  fn expect_term(&mut self) -> Result<Node, mathcore::Error> {
    let cur = self.lexer.consume(); // eating the n | '(' | '+' | '-'

    match cur {
      Token::Number(value, position) => Ok(Node::Number(value, position)),
      Token::LeftPar(_) => self.collect_parentesis(),
      Token::Plus(_) | Token::Minus(_) => self.colect_unary(cur),
      _ => Err(mathcore::Error::from("unknown token".to_string(), cur.get_position()))
    }
  }

  fn expect_factor(&mut self) -> Result<Node, mathcore::Error> {
    self.expect_pattern(Parser::expect_term, &[Token::Star(0..0), Token::Slash(0..0)])
  }

  fn expect_expression(&mut self) -> Result<Node, mathcore::Error> {
    self.expect_pattern(Parser::expect_factor, &[Token::Plus(0..0), Token::Minus(0..0)])
  }

  pub fn parse(&mut self) -> Result<Node, mathcore::Error> {
    let expression = self.expect_expression();
    self.expect_token(Token::Eof(0..0))?;

    expression
  }
}