from Lexer.lexer import Lexer

lexer = Lexer()

raw_code = ''

with open('teste.txt', 'r') as f:
  raw_code = f.read()

lexer.read_next_token(raw_code)

print(lexer)
