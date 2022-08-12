class Token:
  def __init__(self, token: str, lexeme: str, line: int):
    self.token = token
    self.lexeme = lexeme
    self.line = line

  def __str__(self):
    str = f'({self.token}: "{self.lexeme}" - L{self.line}), '
    
    return str

  