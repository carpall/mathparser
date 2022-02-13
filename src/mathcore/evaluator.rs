use crate::mathcore;
use mathcore::Node;
use mathcore::BinaryOperator;
use mathcore::UnaryOperator;

#[derive(Clone)]
pub struct Evaluator {
  parser: mathcore::Parser
}

impl Evaluator {
  pub fn from(expression: String) -> Self {
    Self {
      parser: mathcore::Parser::from(expression)
    }
  }

  fn evaluate_binary(self, op: BinaryOperator, left: Node, right: Node) -> Result<f64, mathcore::Error> {
    let l = self.clone().evaluate_node(left)?;
    let r = self.evaluate_node(right.clone())?;

    match op {
      BinaryOperator::Plus(_) => Ok(l + r),
      BinaryOperator::Minus(_) => Ok(l - r),
      BinaryOperator::Star(_) => Ok(l * r),
      BinaryOperator::Slash(position) => if r == 0f64 {
        Err(mathcore::Error::from("dividing by 0".to_string(), position.start..right.get_position().end))
      } else {
        Ok(l / r)
      }
    }
  }

  fn evaluate_unary(self, op: UnaryOperator, term: Node) -> Result<f64, mathcore::Error> {
    let t = self.evaluate_node(term)?;

    match op {
      UnaryOperator::Plus(_) => Ok(t),
      UnaryOperator::Minus(_) => Ok(-t)
    }
  }

  fn evaluate_node(self, node: Node) -> Result<f64, mathcore::Error> {
    match node {
      Node::Number(number, _) => Ok(number),
      Node::BinaryOperation(op, left, right) => self.evaluate_binary(
        op,
        *left,
        *right
      ),
      Node::UnaryOperation(op, term) => self.evaluate_unary(op, *term)
    }
  }

  pub fn evaluate(&mut self) -> Result<f64, mathcore::Error> {
    self.clone().evaluate_node(self.parser.parse()?)
  }
}