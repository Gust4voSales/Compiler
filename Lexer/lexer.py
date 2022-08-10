from pickle import NONE
from CompilerException import CompilerException
from Lexer.delimiters import DELIMITERS
from Token import Token
from Lexer.reserverd_keywords import RESERVED_KEYWORDS


class Lexer:
  def __init__(self):
    self.tokens: list[Token] = []
    self.char_index = 0
    self.current_line = 1
  
  def is_delimiter(self,char: str):
    for key_token, lexeme_value in DELIMITERS.items():
      if (char == lexeme_value):
        return key_token
    return None

  def read_next_token(self, code: str):
    state = None
    term = ''
    end_of_file = False


    while 1:
      char = code[self.char_index]
      term += char
      self.char_index += 1
      print (state, char)      

      # IGNORE CHAR
      if (char == ' ' or char == '\n'):
        term = term[:-1]
        break
      
   
      # setting current token state 
      match state:
        case None:
          # FOR EXAMPLE: ; { } ( ) 
          if (self.is_delimiter(term)):
            state = 'DELIMITER'
            continue
          if (char.isalpha()):
            state = 'ALPHA'
            continue
          elif (char.isnumeric()):
            state = 'NUMERIC'
            continue
        
        case 'ALPHA':
          if (char.isalpha()):
            print ('char ',char)
            continue
          elif (char.isnumeric()):
            state = 'ALPHANUM'
            continue
          elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1
            print ('char 2',char)
            break
        
        case 'ALPHANUM':
          if (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1
            break
          continue

        case 'NUMERIC':
          if (char.isalpha()):
            raise CompilerException(char, self.current_line)
          elif (char.isnumeric()):
            continue
          elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1
            break

        case 'DELIMITER':
          if (not self.is_delimiter(term)):
            term = term[:-1]
            self.char_index-=1
            break

      if (self.char_index == len(code)):
        end_of_file = True
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
    elif (state == 'DELIMITER'):
      self.tokens.append(Token(token=self.is_delimiter(term), lexeme=term, line=self.current_line))

    if (not end_of_file):
      # increment line
      if (char == '\n'):
        self.current_line+= 1

      self.read_next_token(code)

  def run(self, code: str):

    return 
    

  def __str__(self):
    str = '--------------\n'
    for token in self.tokens:
      str += f'({token.token}: "{token.lexeme}" - L{token.line}), '
    
    return str


