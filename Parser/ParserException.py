class ParserException(Exception):
  def __init__(self, message: str, line: int):            
      # Call the base class constructor with the parameters it needs
      super().__init__(f"Erro de parser na linha {line} \n{message}")