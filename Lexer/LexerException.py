class LexerException(Exception):
  def __init__(self, char: str, line: int):            
      # Call the base class constructor with the parameters it needs
      super().__init__(f"Erro de compilação ao ler \"{char}\" na linha {line}")