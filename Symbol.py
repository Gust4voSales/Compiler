class Symbol:
  def __init__(self, lexeme: str, line: int):
    self.type: str = None
    self.lexeme = lexeme
    self.line = line

  def __str__(self):
    str = '--------------\n'
   
    str += f'({self.type}: "{self.lexeme}" - L{self.line}), '
    
    return str

  