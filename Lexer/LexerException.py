class LexerException(Exception):
  def __init__(self, term: str, line: int):            
      # Call the base class constructor with the parameters it needs
      self.line = line

      super().__init__(f"\"{term}\" termo inválido na linha {line}")