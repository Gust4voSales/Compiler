from Parser.ParserException import ParserException, missing_token_exception_message
from Token import Token
from Symbol import Symbol
from utils.check_token import * 
import three_address_code as three_addrs_code 
from ExpressionToken import ExpressionToken

class Parser:
    def __init__(self, tokens:list[Token], symbols_table:list[Symbol]) -> None:
        self.tokens = tokens
        self.symbols_table = symbols_table
        self.current_token_index = -1
        self.current_symbol_index = -1
        self.scope_stack = []    

        self.is_inside_expression = False
        self.current_expression_tokens = []
    
    # ---------START 3-ADDRESS-CODE FUNCTIONS---------
    def reset_expression_vars(self):
        three_addrs_code.reset()
        self.is_inside_expression = False
        self.current_expression_tokens = []
    
    def get_identifier_type_from_token(self, token: Token):
        sliced_symbols_reversed = self.symbols_table[:self.current_symbol_index][::-1]

        for symbol in sliced_symbols_reversed:
            if (symbol.lexeme == token.lexeme):
                if (symbol.scope == self.scope_stack[-1]):
                    return symbol.type
        return None
        
    # ---------END OF 3-ADDRESS-CODE FUNCTIONS---------
    
    # ---------START SYMBOL TABLE FUNCTIONS---------
    def set_symbol_id(self, id: str):
        self.current_symbol_index += 1
        self.symbols_table[self.current_symbol_index].symbol_id = id

    def set_symbol_type(self, type: str):
        self.symbols_table[self.current_symbol_index].type = type

    def get_symbol_from_identifier(self, idetifier:str):
        
        actual_scope = self.scope_stack[-1]

        sliced_symbols_reversed = self.symbols_table[:self.current_symbol_index][::-1]

        for symbol in sliced_symbols_reversed:
            if (symbol.lexeme==idetifier and symbol.scope == actual_scope):
                return symbol
        return None

    # ---------END SYMBOL TABLE FUNCTIONS---------

    # ---------SCOPE FUNCTIONS---------
    def push_new_scope(self, token: Token):
        self.scope_stack.append(f'{token.lexeme}-{token.line}') # add to scope stack 

    def set_symbol_scope(self, scope=None):
        if not scope:
            self.symbols_table[self.current_symbol_index].scope = self.scope_stack[-1] # scope stack top
        else:
            self.symbols_table[self.current_symbol_index].scope = scope

    # check and set if current symbol is already initialized in a valid scope
    def set_valid_identifier_scope(self):
        scope_found = False
        current_symbol = self.symbols_table[self.current_symbol_index]
        sliced_symbols_reversed = self.symbols_table[:self.current_symbol_index][::-1]

        for symbol in sliced_symbols_reversed:
            if (symbol.lexeme == current_symbol.lexeme):
                if (symbol.scope in self.scope_stack):
                    self.set_symbol_scope(symbol.scope)
                    scope_found = True
                    break

        if not scope_found:
            raise ParserException("Indentificador utilizado não foi declarado no escopo atual", current_symbol.line)
    
    # check if the the given scope is a function in the symbols table
    def is_function_scope(self, scope):
        for symbol in self.symbols_table:
            if(symbol.symbol_id == "FUNCTION_NAME" and str(symbol.lexeme) in scope):
                return True
        return False

    # check if the return is outside a function, then throws an error
    def check_valid_scope_return(self):
        fuction_scope_found = False
        for scope in self.scope_stack[::-1]:
            if(self.is_function_scope(scope)):         
                fuction_scope_found = True
                break
        if not fuction_scope_found:
            raise ParserException("Return fora de função", self.tokens[self.current_token_index].line)

    # check if there is another symbol declaration in the same scope
    def check_unique_symbol_scope(self):
        actual_symbol = self.symbols_table[self.current_symbol_index]
        actual_scope = self.scope_stack[-1]

        sliced_symbols_reversed = self.symbols_table[:self.current_symbol_index][::-1]

        for symbol in sliced_symbols_reversed:
            if (symbol.lexeme==actual_symbol.lexeme and symbol.scope == actual_scope):
                raise ParserException('Declaração repetida', actual_symbol.line)
    # ---------END SCOPE FUNCTIONS---------

    # helper function to check (based on id) if sub_routine is a function or a procedure when called to put correct type
    # in symbols table
    def get_symbol_with_same_identifier(self, identifier: str):
        for symbol in self.symbols_table:
            if (symbol.lexeme == identifier):
                return symbol
        return None

    def look_ahead(self, quantity=1):
        self.current_token_index += quantity
        if (self.current_token_index <= len(self.tokens)-1):
            token = self.tokens[self.current_token_index]
            self.current_token_index -= quantity
            return token
        else:
            self.current_token_index -= quantity
            return Token(token='EMPTY', lexeme='', line=0)

    def read_token(self):
        self.current_token_index += 1
        if (self.current_token_index <= len(self.tokens)-1):
            token = self.tokens[self.current_token_index]
            
            if (self.is_inside_expression):
                if is_identifier(token):
                    symbol = self.get_symbol_with_same_identifier(token.lexeme)
                    if symbol.symbol_id == "FUNCTION_NAME" or symbol.symbol_id == "PROCEDURE_NAME":
                        self.current_expression_tokens.append(ExpressionToken(token,self.get_identifier_type_from_token(token), symbol.parameters_type))
                    else:
                        self.current_expression_tokens.append(ExpressionToken(token,self.get_identifier_type_from_token(token)))
                else:
                    self.current_expression_tokens.append(ExpressionToken(token))
                

            return token 
        else:
            self.current_token_index -= 1
            return Token(token='EMPTY', lexeme='', line=-99999)

    def semicolon(self): #ok
        token = self.read_token()
        if (not token.token == 'SEMICOLON'):
            raise ParserException(f"Faltou \";\" antes do {self.tokens[self.current_token_index].lexeme}", self.tokens[self.current_token_index].line)

    def identifier(self): # ok
        identifier = self.read_token() # read identifier
        if (not is_identifier(identifier)):
            raise ParserException(f"{identifier.lexeme} não é um nome de identificador válido", identifier.line)
        
        return identifier

    # --------START BODIES--------
    def program(self): # ok
        token = self.read_token() #read program

        if(not token.token =="HEADER_PROGRAM"): 
            raise ParserException(missing_token_exception_message("program"), token.line)

        identifier = self.identifier()
        self.set_symbol_id('PROGRAM_NAME')
        self.push_new_scope(identifier) # add to scope stack 

        if (not self.read_token().token == "OPEN_BRACKET"): #read {
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.body()

        if (not self.read_token().token == "CLOSE_BRACKET"): #read }
            raise ParserException(missing_token_exception_message("}"), token.line)
        
        self.scope_stack.pop() # pop from scope stack

    def body(self): # ok
        self.var_declaration_block()
        self.sub_routines_declaration()
        self.commands()

    def sub_routine_body(self): # ok
        self.var_declaration_block()

        self.commands()
    # --------END BODIES--------

    # --------START EXPRESSION--------
    def factor(self): 
        token = self.read_token()  
        function_call = False

        # (<expression>) 
        if (token.lexeme=='('):
            self.expression()
            token = self.read_token()  
            if (not (token.lexeme==')')):
                raise ParserException(missing_token_exception_message(")"), token.line)
        elif(is_identifier(token) and self.look_ahead().token == "OPEN_PARENTHESES"):
            self.set_symbol_id("FUNCTION_NAME")
            symbol = self.get_symbol_from_identifier(token.lexeme)
            if (symbol):
                self.set_symbol_type(symbol.type)

            self.function_call(True)
            function_call = True
        elif (not (is_identifier(token) or is_number(token) or is_boolean(token)) ):
            raise ParserException('Faltou fator', token.line)
        
        if (not function_call and is_identifier(token)): # a variable identifier was used    
            self.set_symbol_id("VARIABLE_NAME")
            self.set_valid_identifier_scope()
        
    def term(self): # ok ?
        self.factor()
        while (self.look_ahead().lexeme == '*' or self.look_ahead().lexeme == '/' or self.look_ahead().lexeme == '&&' ):
            self.term_line()

    def term_line(self): # ok
        self.read_token() # reading * / &&
        self.factor()

    def simple_expression(self): # ok
        if (self.look_ahead().lexeme == '+' or self.look_ahead().lexeme == '-'):
            self.read_token()
        
        self.term()

        while (self.look_ahead().lexeme == '+' or self.look_ahead().lexeme == '-' or self.look_ahead().lexeme == '||' ):
            self.simple_expression_line()        

    def simple_expression_line(self): # ok
        self.read_token()
        self.term()

    def expression(self): # ok?
        self.simple_expression()

        if (is_relation_op(self.look_ahead())):
            self.read_token() # read relational op
            self.expression()

    # --------END EXPRESSION--------
    
    # --------START DECLARATIONS--------
    def sub_routines_declaration(self):
        look_ahead = self.look_ahead()
        while(look_ahead.token =="HEADER_FUNC" or look_ahead.token =="HEADER_PROC"):
            if (look_ahead.token =="HEADER_FUNC"):
                self.function_declaration()
            elif(look_ahead.token == "HEADER_PROC"):
                self.procedure_declaration()
            look_ahead = self.look_ahead()

    def type(self): # ok
        token = self.read_token()
        if (not (token.token == 'INT_TYPE' or token.token == 'BOOL_TYPE')):
            raise ParserException(f"Tipo {token.lexeme} inválido", token.line)

        return token
    
    def var_declaration_block(self): # ok
        look_ahead = self.look_ahead()
        while (look_ahead.token == "INT_TYPE" or look_ahead.token == "BOOL_TYPE"):
            self.var_declaration()
            look_ahead = self.look_ahead()

    def var_declaration(self): # ok
        token_type = self.type()
        self.identifier()

        self.set_symbol_id("VARIABLE_NAME")
        self.set_symbol_type(token_type.token)
        self.set_symbol_scope()
        self.check_unique_symbol_scope()

        while (self.look_ahead().lexeme==','):
            self.read_token() # read ,
            self.identifier()
            self.set_symbol_id("VARIABLE_NAME")

        self.semicolon()  

    def parameter(self, subroutine_symbol_index: int): # ok
        token_type= self.type() 
        self.identifier()
        self.set_symbol_id("VARIABLE_NAME")
        self.set_symbol_type(token_type.token)
        self.set_symbol_scope()
        self.check_unique_symbol_scope()

        # add its type to the subroutines parameters_list_type 
        self.symbols_table[subroutine_symbol_index].parameters_type.append(token_type.token)

    def parameters_list(self, subroutine_symbol_index: int): # ok
        look_ahead = self.look_ahead()
        if (look_ahead.token == "BOOL_TYPE" or look_ahead.token == "INT_TYPE"):
            self.parameter(subroutine_symbol_index)  
            while (self.look_ahead().lexeme==','):
                self.read_token() # read ,
                self.parameter(subroutine_symbol_index)
  
    def procedure_declaration(self): # ok 
        token = self.read_token() # read proc

        if (not token.token == "HEADER_PROC"):
            raise ParserException(f"Verificação com look ahead??? Era pra ler o proc", token.line)
        
        identifier = self.identifier()
        self.set_symbol_id("PROCEDURE_NAME")
        self.set_symbol_scope()
        self.check_unique_symbol_scope()
        self.push_new_scope(identifier) # add to scope stack

        token = self.read_token() # read (
        if (not token.token == "OPEN_PARENTHESES"):
            raise ParserException(missing_token_exception_message("("), token.line)
        
        self.parameters_list(self.current_symbol_index)

        token = self.read_token() # read )
        if (not token.token == "CLOSE_PARENTHESES"):
            raise ParserException(missing_token_exception_message(")"), token.line)
        
        token = self.read_token() # read {
        if (not token.token == "OPEN_BRACKET"):
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.sub_routine_body()

        token = self.read_token() # read }
        if (not token.token == "CLOSE_BRACKET"):
            raise ParserException(missing_token_exception_message("}"), token.line)
        
        self.scope_stack.pop() # pop from scope stack

    def function_declaration(self): # ok 
        token = self.read_token() # read func

        if (not token.token == "HEADER_FUNC"):
            raise ParserException(f"Verificação com look ahead??? Era pra ler o func", token.line)
        
        type_token = self.type()
        identifier = self.identifier()
        self.set_symbol_id("FUNCTION_NAME")
        self.set_symbol_scope()
        self.set_symbol_type(type_token.token)
        self.check_unique_symbol_scope()
        self.push_new_scope(identifier) # add to scope stack

        token = self.read_token() # read (
        if (not token.token == "OPEN_PARENTHESES"):
            raise ParserException(missing_token_exception_message("("), token.line)
        
        self.parameters_list(self.current_symbol_index)

        token = self.read_token() # read )
        if (not token.token == "CLOSE_PARENTHESES"):
            raise ParserException(missing_token_exception_message(")"), token.line)
        
        token = self.read_token() # read {
        if (not token.token == "OPEN_BRACKET"):
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.sub_routine_body()
        

        token = self.read_token() # read }
        if (not token.token == "CLOSE_BRACKET"):
            raise ParserException(missing_token_exception_message("}"), token.line)
        
        self.scope_stack.pop() # pop from scope stack

    # --------END DECLARATIONS--------

    # --------START COMMAND--------
    def commands(self): # ok
        previous_read_token = self.look_ahead().token
        self.command()
        while (self.look_ahead().token != "CLOSE_BRACKET"):
            previous_read_token = self.look_ahead().token
            self.command()
            
        #if the current scope is a function, and the previous saved command wasn't a return, throw an error
        if (self.is_function_scope(self.scope_stack[-1]) and not(previous_read_token == "RETURN")):
            raise ParserException(missing_token_exception_message("return"), self.tokens[self.current_token_index].line)

    def command(self):
        look_ahead_token = self.look_ahead()
        if (look_ahead_token.token=='PRINT_FUNC'):
            self.print_command()
        elif (look_ahead_token.token == "INPUT_FUNC"):
            self.input_command()
        elif (look_ahead_token.token == "BREAK"):
            self.break_command()
        elif (look_ahead_token.token == "CONTINUE"):
            self.continue_command()
        elif (look_ahead_token.token == "RETURN"):
            self.return_command()
        elif (look_ahead_token.token == "WHILE"):
            self.while_command()
        elif (look_ahead_token.token == "IF"):
            self.conditional_command()
        elif (look_ahead_token.token == "IDENTIFIER"): # attribution or function/procedure commands
            second_look_ahead = self.look_ahead(2)
            if (second_look_ahead.token == 'ASSIGNMENT_OP'):  
                self.var_attribution()
            elif (second_look_ahead.token == 'OPEN_PARENTHESES'):
                self.sub_routine_call() # procedures and functions calls
            else:
                raise ParserException(f"Comando \"{look_ahead_token.lexeme}\" inválido", look_ahead_token.line)
        else:
            raise ParserException(f"Comando \"{look_ahead_token.lexeme}\" inválido", look_ahead_token.line)

    def var_attribution(self): # ok
        token_identifier =self.identifier()
        symbol = self.get_symbol_from_identifier(token_identifier.lexeme)

        self.set_symbol_id("VARIABLE_NAME")
        self.set_valid_identifier_scope()

        self.set_symbol_type(symbol.type)

        assign_op = self.read_token() # read =
        if (not (assign_op.token == 'ASSIGNMENT_OP')):
            raise ParserException(f"Atribuição inválida: {assign_op.lexeme}", assign_op.line)
        
        if(self.look_ahead().token == "INPUT_FUNC"):
            self.input_command()
            three_addrs_code.parse_command(f"{token_identifier.lexeme} = input()")
        else:
            self.is_inside_expression = True 
            self.expression()
            three_addrs_code.parseExpression(self.current_expression_tokens)    
            three_addrs_code.parse_var_attribution(symbol)
            self.reset_expression_vars()
            self.semicolon()

    def print_command(self): # ok
        token = self.read_token() #read print

        if(not token.token =="PRINT_FUNC"): 
            raise ParserException(f"Verificação com look ahaed???", token.line)
        elif(not self.read_token().token == "OPEN_PARENTHESES"): #read (
            raise ParserException(missing_token_exception_message("("), token.line)

        
        
        self.is_inside_expression = True 
        self.expression()
        three_addrs_code.parseExpression(self.current_expression_tokens)
        three_addrs_code.parse_command("print(#)")
        self.reset_expression_vars()

        if (not self.read_token().token == "CLOSE_PARENTHESES"): #read )
            raise ParserException(missing_token_exception_message(")"), token.line)

        self.semicolon()

    def while_command(self): # ok
        token = self.read_token() #read while   

        self.push_new_scope(token) # add to scope stack

        if(not token.token =="WHILE"): 
            raise ParserException(f"Verificação com look ahaed???", token.line)
        elif(not self.read_token().token == "OPEN_PARENTHESES"): #read (
            raise ParserException(missing_token_exception_message("("), token.line)

        self.is_inside_expression = True 
        self.expression()
        three_addrs_code.parseExpression(self.current_expression_tokens)
        three_addrs_code.parse_while_command()
        self.reset_expression_vars()
        

        if (not self.read_token().token == "CLOSE_PARENTHESES"): #read )
            raise ParserException(missing_token_exception_message(")"), token.line)

        if (not self.read_token().token == "OPEN_BRACKET"): #read {
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.var_declaration_block()
        self.commands()

        if (not self.read_token().token == "CLOSE_BRACKET"): #read }
            raise ParserException(missing_token_exception_message("}"), token.line)

        three_addrs_code.add_while_final_labels()
        self.scope_stack.pop() # pop from scope stack
         
    def input_command(self): # ok
        token = self.read_token() #read input

        if(not token.token =="INPUT_FUNC"): 
            raise ParserException(f"Verificação com look ahaed??", token.line)
        elif(not self.read_token().token == "OPEN_PARENTHESES"): #read (
            raise ParserException(missing_token_exception_message("("), token.line)
        elif (not self.read_token().token == "CLOSE_PARENTHESES"): #read )
            raise ParserException(missing_token_exception_message(")"), token.line)

        self.semicolon()

    def break_command(self): # ok 
        token = self.read_token() #read break
        if(not token.token == "BREAK"):
            raise ParserException(f"Verificação com look ahaed???", token.line)
        self.semicolon()

    def continue_command(self): # ok
        token = self.read_token() #read continue
        if(not token.token == "CONTINUE"):
            raise ParserException(f"Verificação com look ahaed???", token.line)
        self.semicolon()

    def return_command(self): # ok
        token = self.read_token() #read return
        self.check_valid_scope_return()

        if(not token.token == "RETURN"):
            raise ParserException(missing_token_exception_message("return"), token.line)
        self.expression()
        self.semicolon()            

    def sub_routine_call(self): # ok
        subroutine_identifier = self.identifier()
        sub_routine_symbol = self.get_symbol_with_same_identifier(self.tokens[self.current_token_index].lexeme)
        self.set_symbol_id(sub_routine_symbol.symbol_id)
        self.set_symbol_type(sub_routine_symbol.type)
        self.set_valid_identifier_scope()

        token = self.read_token() # read (
        if (not token.token == 'OPEN_PARENTHESES'):
            raise ParserException(missing_token_exception_message("("), token.line)
        
        parameters_counter = 0
        look_ahead = self.look_ahead() # check obrigatory ) or optionals expressions (separated by comma)
        while (not look_ahead.token == 'CLOSE_PARENTHESES'):
            self.expression()
            parameters_counter += 1

            look_ahead = self.look_ahead() # check obrigatory ) or optional comma
            if (look_ahead.lexeme == ','):
                self.read_token() # read ,
        else:
            token = self.read_token() # read )
            if (not look_ahead.token == 'CLOSE_PARENTHESES'):
                raise ParserException(missing_token_exception_message(")"), token.line)

        subroutine_symbol = self.get_symbol_with_same_identifier(subroutine_identifier.lexeme)
        if (parameters_counter != len(subroutine_symbol.parameters_type)):
            raise ParserException("Quantidade de parâmetros passados diferentes da declaração", subroutine_identifier.line)
        self.semicolon()

    # only being called inside expression because outside an expression functions are called through sub_routine_call
    def function_call(self, in_expression = False): # ok 
        if not in_expression:
            token_identifier = self.identifier()
            self.set_symbol_id("FUNCTION_NAME")
            symbol = self.get_symbol_from_identifier(token_identifier.lexeme)
            self.set_symbol_type(symbol.type)

       
        self.set_valid_identifier_scope()
        subroutine_identifier = self.symbols_table[self.current_symbol_index]

        token = self.read_token() # read (
        if (not token.token == 'OPEN_PARENTHESES'):
            raise ParserException(missing_token_exception_message("("), token.line)

        parameters_counter = 0
        look_ahead = self.look_ahead() # check obrigatory ) or optionals expressions (separated by comma)
        while (not look_ahead.token == 'CLOSE_PARENTHESES'):
            self.expression()
            parameters_counter += 1

            look_ahead = self.look_ahead() # check obrigatory ) or optional comma
            if (look_ahead.lexeme == ','):
                self.read_token() # read ,
        else:
            token = self.read_token() # read )
            if (not look_ahead.token == 'CLOSE_PARENTHESES'):
                raise ParserException(missing_token_exception_message(")"), token.line)

        subroutine_symbol = self.get_symbol_with_same_identifier(subroutine_identifier.lexeme)
        if (parameters_counter != len(subroutine_symbol.parameters_type)):
            raise ParserException("Quantidade de parâmetros passados diferentes da declaração", subroutine_identifier.line)

        if(not in_expression):
            self.semicolon()

    def conditional_command(self): # ok
        token = self.read_token() #read if
        
        self.push_new_scope(token) # add to scope stack 
        conditional_scope = self.scope_stack[-1]

        if(not token.token == "IF"): 
            raise ParserException(f"Verificação com look ahaed???", token.line)
        elif(not self.read_token().token == "OPEN_PARENTHESES"): #read (
            raise ParserException(missing_token_exception_message("("), token.line)

        self.is_inside_expression = True 
        self.expression()
        three_addrs_code.parseExpression(self.current_expression_tokens)

        three_addrs_code.parse_if_command(conditional_scope)
        self.reset_expression_vars()
        

        if (not self.read_token().token == "CLOSE_PARENTHESES"): #read )
            raise ParserException(missing_token_exception_message(")"), token.line)

        if (not self.read_token().token == "OPEN_BRACKET"): #read {
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.var_declaration_block()
        self.commands()

        if (not self.read_token().token == "CLOSE_BRACKET"): #read }
            raise ParserException(missing_token_exception_message("}"), token.line)
        
        self.scope_stack.pop() # pop from scope stack
        

        if (self.look_ahead().token == "ELSE"):            
            token = self.read_token() # read else

            self.push_new_scope(token) # add to scope stack

            if (not self.read_token().token == "OPEN_BRACKET"): #read {
                raise ParserException(missing_token_exception_message("{"), token.line)
            
            three_addrs_code.parse_else_command(conditional_scope)
            self.var_declaration_block()
            self.commands()

            if (not self.read_token().token == "CLOSE_BRACKET"): #read }
                raise ParserException(missing_token_exception_message("}"), token.line)
            
            three_addrs_code.add_final_conditional_command(conditional_scope, True)
            self.scope_stack.pop()
        else:
            three_addrs_code.add_final_conditional_command(conditional_scope, False)
        

    # --------END COMMAND--------
    
