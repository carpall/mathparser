use crate::mathcore::Position;

pub struct Error {
  pub message: String,
  pub position: Position
}

impl Error {
  pub fn from(message: String, position: Position) -> Self {
    Self {
      message,
      position
    }
  }
}