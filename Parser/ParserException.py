class ParserException(Exception):
  def __init__(self, message: str, line: int):            
      self.line = line
      # Call the base class constructor with the parameters it needs
      super().__init__(f"{message} na linha {line}")


def missing_token_exception_message(token: str):
  return f"\"{token}\" esperado"