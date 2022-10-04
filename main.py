from Lexer.LexerException import LexerException
from Lexer.lexer import Lexer
from Parser.ParserException import ParserException
from Parser.parser import Parser
import os

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

if os.path.exists("3-address-code.txt"):
  os.remove("3-address-code.txt")


try:
  lexer = Lexer(raw_code)

  tokens, symbols = lexer.run()
  # print(lexer)
  parser = Parser(tokens, symbols)

  parser.program()

  # print("---------------------TOKENS---------------------")
  # for token in tokens:
  #   print(token)
  # print('\n')

  print("---------------------Tabela de Simbolos---------------------")
  for s in parser.symbols_table:
    print(s)
  print('\n')

except LexerException as e:
  lines = raw_code.splitlines()
  print(bcolors.FAIL + str(e))
  print(f"{bcolors.FAIL}{e.line}. {lines[e.line-1]}{bcolors.ENDC}")
except ParserException as e:
  lines = raw_code.splitlines()
  print(bcolors.FAIL + str(e))
  print(f"{bcolors.FAIL}{e.line}. {lines[e.line-1]}{bcolors.ENDC}")
