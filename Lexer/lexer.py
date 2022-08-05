from Token import Token
from Lexer.reserverd_keywords import RESERVED_KEYWORDS

class Lexer:
  def __init__(self):
    self.tokens: list[Token] = []
    self.char_index = 0
    self.current_line = 1

  def read_next_token(self, code: str):
    state = None
    term = ''
    end = False

    while 1:
      char = code[self.char_index]
      term += char
      self.char_index += 1
      print (state, char)      

      # IGNORE CHAR
      if (char == ' ' or char == '\n'):
        term = term[:-1]
        break

      elif (state==None):
        # FOR EXAMPLE: ; { } ( ) 
        # if (isDelimitador(char)):
        #   state = 'DELIMITADOR'
        #   break
        if (char.isalpha()):
          state = 'ALPHA'
          continue
        elif (char.isnumeric()):
          state = 'NUMERIC'
          continue

      elif (state=='ALPHA'):
        if (char.isalpha()):
          continue
        elif (char.isnumeric()):
          state = 'ALPHANUM'
          continue
      
      elif (state=='ALPHANUM'):
        continue

      elif (state == 'NUMERIC'):
        if (char.isalpha()):
          print("ERROR")
          return
        elif (char.isnumeric()):
          continue

      if (self.char_index == len(code)):
        end = True
        break


    # CAN BE RESERVED KEY_WORD OR IDENTIFIER
    if (state == 'ALPHA'):
      keyword = False
      for key_token, lexeme_value in RESERVED_KEYWORDS.items():
        if (term == lexeme_value):
          self.tokens.append(Token(token=key_token, lexeme=term, line=self.current_line))
          keyword = True
          break
      if (not keyword):
        self.tokens.append(Token(token='IDENTIFIER', lexeme=term, line=self.current_line))
    # IDENTIFIER
    elif (state == 'ALPHANUM'):
      self.tokens.append(Token(token='IDENTIFIER', lexeme=term, line=self.current_line))
    # NUMERIC
    elif (state == 'NUMERIC'):
      self.tokens.append(Token(token='NUMERIC', lexeme=term, line=self.current_line))

    if (not end):
      self.read_next_token(code)

  def run(self, code: str):

    return 
    for char in code:
      if (char=='\n' ):
        self.current_line += 1
        print('pula linha')
        continue

      if (char==' '):
        print('vazio')
        continue
      
      if (char == ';'):
        print(char)
        self.tokens.append(Token(token='SEMICOLON', lexeme=char, line=self.current_line))
        continue
      
      if (char=='{'):
        print(char)
        self.tokens.append(Token(token='OPEN_BRACKETS', lexeme=char, line=self.current_line))
        continue

      if (char=='}'):
        print(char)
        self.tokens.append(Token(token='CLOSE_BRACKETS', lexeme=char, line=self.current_line))
        continue
    
      if (char=='('):
        print(char)
        self.tokens.append(Token(token='OPEN_PARENTESES', lexeme=char, line=self.current_line))
        continue

      if (char==')'):
        print(char)
        self.tokens.append(Token(token='CLOSE_PARENTESES', lexeme=char, line=self.current_line))
        continue

  def __str__(self):
    str = '--------------\n'
    for token in self.tokens:
      str += f'({token.token}: "{token.lexeme}" - {token.line}), '
    
    return str


