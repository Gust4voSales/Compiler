from Token import Token


class ExpressionToken (Token):
  def __init__(self, token: Token, type: str = None):
    super().__init__(token.token, token.lexeme, token.line)
    self.type = type

  def __str__(self):
    str = f'({self.token}: "{self.lexeme}" - L{self.line} - type:{self.type}), '
    
    return str


