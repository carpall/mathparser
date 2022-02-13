use std::io::{Write};
mod mathcore;

fn print_error(error: mathcore::Error) {
  let mut stderr = std::io::stderr();

  // padding, with overhead of '> '
  for _ in 0 .. error.position.start + 2 { write!(stderr, " ").unwrap(); }

  // writing ~~~~
  for _ in error.position { write!(stderr, "-").unwrap(); }

  writeln!(stderr, " {}", error.message).unwrap();
}

fn main() {
  loop {
    let mut expression = String::new();

    print!("> ");
    std::io::stdout().flush().unwrap();
    std::io::stdin().read_line(&mut expression).unwrap();

    expression.pop(); // removing \n from the head

    if expression.len() == 0 { continue; } // skipping empty expressions

    let evaluted_result = mathcore::Evaluator::from(expression.clone()).evaluate();

    match evaluted_result {
      Ok(result) => println!("{}", result),
      Err(error) => print_error(error),
    }
  }
}