from Token import Token

temp_index = 0
expression=[]

def generate_temp_expressions(expression_tokens_list, precedence_operator: str):
  global temp_index
  new_expressions_tokens_list = []

  for index, token in enumerate(expression_tokens_list):
    # if the token with precedence has been found we need to save the expression using it in an temp 
    if token.token == precedence_operator:
      # temp = <PREVIOUS_TOKEN> <OPERATOR> <NEXT_TOKEN>
      # eg.: calling generate_temp_expressions with 2+2*5 and the precedence_operator='*' 
      # we're going to write -> temp = 2*5
      print(f'temp{temp_index} = {new_expressions_tokens_list[-1].lexeme} {token.lexeme} {expression_tokens_list[index+1].lexeme}')

      # we used the previous token in this expression, so we need to delete it from new_expressions_tokens_list
      del new_expressions_tokens_list[-1]

      # we also use the next token to be read in this expression, so we need to delete it from the array we are iterating
      del expression_tokens_list[index+1]

      # we need to replace the expression we have just read as temp in our new_expressions_tokens_list 
      temp_token = Token(lexeme=f'temp{temp_index}', token=None, line=None)
      new_expressions_tokens_list.append(temp_token)
      temp_index+=1
    else:
      new_expressions_tokens_list.append(token)
  
  return new_expressions_tokens_list



def parseExpression(expression_tokens_list: list[Token]):
  # expression separated by delimiters
  precedence_operator_order = ['MULT',
  'DIV',
  'ADD',
  'LESS',
  'LESS_THAN_OP',
  'LESS_OR_EQ_OP',
  'GREATER_THAN_OP',
  'GREATER_OR_EQ_OP',
  'EQUALS_OP',
  'NOT_EQUAL_OP',
  'AND',
  'OR']

  open_parentheses_index= -1
  close_parentheses_index= -1

  # seting index for the first open parentheses 
  for index, token in enumerate(expression_tokens_list):
    if token.token == 'OPEN_PARENTHESES':
      open_parentheses_index = index
      break

  # seting index for the last close parentheses    
  for index, token in enumerate(expression_tokens_list):
    if token.token == 'CLOSE_PARENTHESES':
      close_parentheses_index = index

  # if the we have open parentheses recursively then call parseExpression with the expression 
  # inside the ( ) 
  if open_parentheses_index > -1:
    parseExpression(expression_tokens_list[open_parentheses_index+1:close_parentheses_index:])
    

  # if exist a parentheses, then we have called parseExpression recursively right up 
  # so we replace the expression from inside ( ) for temp
  if close_parentheses_index >-1:
    temp_token = Token(lexeme=f'temp{temp_index-1}', token=None, line=None)
    expression_tokens_list = expression_tokens_list[:open_parentheses_index:] + [temp_token] + expression_tokens_list[close_parentheses_index+1::]
   
  # iterates the operators in the precedence order and generates temps expressions
  for precedence in precedence_operator_order:
    expression_tokens_list = generate_temp_expressions(expression_tokens_list, precedence)


 
  