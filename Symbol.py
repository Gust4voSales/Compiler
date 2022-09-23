class Symbol:
  def __init__(self, lexeme: str, line: int):
    self.lexeme = lexeme
    self.line = line
    self.symbol_id: str = None
    self.scope: str = None
    self.type: str = None

  def __str__(self):
    str = f'({self.symbol_id}: "{self.lexeme}" - L{self.line}), SCOPE: {self.scope}, TYPE: {self.type}'
    
    return str

  