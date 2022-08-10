from CompilerException import CompilerException
from Lexer.lexer import Lexer

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

lexer = Lexer()

raw_code = ''

with open('teste.txt', 'r') as f:
  raw_code = f.read()

try:
  lexer.read_next_token(raw_code)
  # print(lexer)

except Exception as e:
  print(bcolors.FAIL + str(e) + bcolors.ENDC)

print(lexer)

