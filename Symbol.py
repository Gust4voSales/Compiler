class Symbol:
  def __init__(self, lexeme: str, line: int):
    self.lexeme = lexeme
    self.line = line
    self.symbol_id: str = None
    self.scope: str = None
    self.type: str = None
    self.parameters_type: list[str] = []

  def __str__(self):
    parameters_type_str = 'PARAMETERS_TYPE: ' if len(self.parameters_type) else ''
    for parameter_type in self.parameters_type:
      parameters_type_str += f'{parameter_type}, '

    str = f'({self.symbol_id}: "{self.lexeme}" - L{self.line}), SCOPE: {self.scope}, TYPE: {self.type}, {parameters_type_str}'
    
    return str

  