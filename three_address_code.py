from Token import Token

temp_index = 0

def generate_temp_expressions(expression_tokens_list: list[Token], precedence_operator: str):
  global temp_index
  new_expressions_tokens_list = []

  # if the expression is of only one factor and it is a temp, don't do anything. Eg: temp5
  if len(expression_tokens_list)==1 and 'temp' in expression_tokens_list[0].lexeme and expression_tokens_list[0].token == None:
    return []

  # expression of only one factor. Eg.: print(2);
  if (len(expression_tokens_list)==1):
    print(f'temp{temp_index} = {expression_tokens_list[0].lexeme}')
    temp_index += 1
    return []

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

def generate_function_parameters(expression_tokens_list: list[Token], index: int):
  global temp_index
  
  temp_params: list[str] = []

  params: list[Token] = [] 
  n_params = 0

  # if there are parameters
  if not expression_tokens_list[index+2].token == "CLOSE_PARENTHESES":
    # iterate through tokens 
    for token_expression_param in expression_tokens_list[index+2:]:
      # end of parameters list
      if token_expression_param.token == "CLOSE_PARENTHESES":
        break
      
      # another parameter expression found, so we execute the first parameters expression and then keep going
      if (token_expression_param.token == "COMMA"):
        parseExpression(params)
        temp_params.append(f'param temp{temp_index-1}')
        params = []
        continue
      
      params.append(token_expression_param)

    # execute the parameter
    parseExpression(params)
    temp_params.append(f'param temp{temp_index-1}')


  return temp_params

def generate_function_call(expression_tokens_list: list[Token]):
  global temp_index

  for index, token in enumerate(expression_tokens_list):
    if (token.token == "IDENTIFIER"):
      is_last_token = index == len(expression_tokens_list)-1
      if (not is_last_token and expression_tokens_list[index+1].token == "OPEN_PARENTHESES"):
        # if we have parameters then call parse expressions for each one
        temp_params = generate_function_parameters(expression_tokens_list, index)

        # execute function and replace its call for temp
        for temp_param in temp_params:
          print(temp_param)
        print(f"temp{temp_index} = call {token.lexeme}, {len(temp_params)}")
        temp_index += 1
        
        expression_tokens_list[index] = Token(lexeme=f'temp{temp_index-1}', token=None, line=None)

        # delete everything between the ( ) and the ( ) as well
        for token in expression_tokens_list[index+1:]:
          if token.token == "CLOSE_PARENTHESES":
            del expression_tokens_list[index+1]
            break

          del expression_tokens_list[index+1]

def parseExpression(expression_tokens_list: list[Token]):
  # check if there are functions calls and execute function calls first
  generate_function_call(expression_tokens_list)

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


 