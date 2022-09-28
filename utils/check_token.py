from Token import Token

def is_identifier(token: Token):
  return token.token == 'IDENTIFIER'
def is_boolean(token: Token):
  return (token.token == 'TRUE' or token.token == 'FALSE')
def is_number(token: Token):
  return token.token == 'NUMERIC'
def is_relation_op(token: Token):
  return (token.lexeme == '!=' or token.lexeme == '==' or token.lexeme == '<' or token.lexeme == '<=' or token.lexeme == '>' or token.lexeme == '>=')
