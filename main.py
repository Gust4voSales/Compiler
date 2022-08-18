from Lexer.LexerException import LexerException
from Lexer.lexer import Lexer
from Parser.ParserException import ParserException
from Parser.parser import Parser

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

raw_code = ''

with open('teste.txt', 'r') as f:
  raw_code = f.read()

try:
  lexer = Lexer(raw_code)

  tokens, symbols = lexer.run()
  # print(lexer)
  parser = Parser(tokens, symbols)

  parser.program()
  for s in parser.symbols_table:
    print(s)

  
except LexerException as e:
  print('lexico')
  print(bcolors.FAIL + str(e) + bcolors.ENDC)
except ParserException as e:
  print('sintatico')
  print(bcolors.FAIL + str(e) + bcolors.ENDC)

# for token in tokens:
#   print(token)

# print('-------------------------------------')
# for id in ids:
#   print(id)


