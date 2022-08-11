from pickle import NONE
from CompilerException import CompilerException
from Identifier import Identifier
from Lexer.delimiters import DELIMITERS
from Token import Token
from Lexer.reserverd_keywords import RESERVED_KEYWORDS


class Lexer:
  def __init__(self, code: str):
    self.tokens: list[Token] = []
    self.ids_table: list[Identifier] = []
    self.char_index = 0
    self.current_line = 1
    self.code = code
  
  def is_delimiter(self,char: str):
    for key_token, lexeme_value in DELIMITERS.items():
      if (char == lexeme_value):
        return key_token
    return None

  def read_next_token(self):
    state = None
    term = ''
    end_of_file = False

    while 1:
      if (self.char_index == len(self.code)):
        end_of_file = True
        break

      char = self.code[self.char_index]
      term += char
      self.char_index += 1
      print(f"state anterior: {state} - char '{char}'")

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
          # don't do anything because it can be the start of a delimiter like "!= || &&"
          elif (char == "!" or char == '|' or char == '&'): 
            continue
          else:
            raise CompilerException(term, self.current_line)
        
        case 'ALPHA':
          if (char.isalpha()):            
            continue
          elif (char.isnumeric()):
            state = 'ALPHANUM'
            continue
          elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1          
            break
          else:
            raise CompilerException(term, self.current_line)
        
        case 'ALPHANUM':
          if (char.isalnum()): continue
          elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1
            break
          else:
            raise CompilerException(term, self.current_line)
            
        case 'NUMERIC':
          if (char.isnumeric()):
            continue
          elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1
            break
          else:
            raise CompilerException(term, self.current_line)

        case 'DELIMITER':
          if (not self.is_delimiter(term)):
            term = term[:-1]
            self.char_index-=1
            break        
    
    if (state == None):
      if (not (term == ' ' or term == '\n' or term=='' or term =='\t')):
        raise CompilerException(term, self.current_line)

    self.add_token_based_on_state(term, state)

    if (not end_of_file):
      # increment line
      if (char == '\n'):
        self.current_line+= 1

      self.read_next_token()

  def run(self):
    self.read_next_token()
    return self.tokens, self.ids_table

  def add_token_based_on_state(self, lexeme: str, state: str):
     # CAN BE RESERVED KEY_WORD OR IDENTIFIER
    if (state == 'ALPHA'):
      keyword = False
      for key_token, lexeme_value in RESERVED_KEYWORDS.items():
        if (lexeme == lexeme_value):
          self.tokens.append(Token(token=key_token, lexeme=lexeme, line=self.current_line))
          keyword = True
          break
      if (not keyword):
        self.tokens.append(Token(token='IDENTIFIER', lexeme=lexeme, line=self.current_line))
        self.ids_table.append(Identifier(token='IDENTIFIER', lexeme=lexeme, line=self.current_line))
    # IDENTIFIER
    elif (state == 'ALPHANUM'):
      self.tokens.append(Token(token='IDENTIFIER', lexeme=lexeme, line=self.current_line))
      self.ids_table.append(Identifier(token='IDENTIFIER', lexeme=lexeme, line=self.current_line))
    # NUMERIC
    elif (state == 'NUMERIC'):
      self.tokens.append(Token(token='NUMERIC', lexeme=lexeme, line=self.current_line))
    elif (state == 'DELIMITER'):
      self.tokens.append(Token(token=self.is_delimiter(lexeme), lexeme=lexeme, line=self.current_line))




