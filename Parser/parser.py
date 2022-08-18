from Parser.ParserException import ParserException, missing_token_exception_message
from Token import Token
from Symbol import Symbol

class Parser:
    def __init__(self, tokens:list[Token], symbols_table:list[Symbol]) -> None:
        self.tokens = tokens
        self.symbols_table = symbols_table
        self.current_token_index = -1
        self.current_symbol_index = -1
    
     
    def set_symbol_type(self, type: str):
        self.current_symbol_index += 1
        self.symbols_table[self.current_symbol_index].type = type

    # helper function to check (based on id) if sub_routine is a function or a procedure when called to put correct type
    # in symbols table
    def is_function_or_procedure(self, identifier: str):
        for symbol in self.symbols_table:
            if (symbol.lexeme == identifier):
                return symbol.type
        return None
        

    def look_ahead(self, quantity=1):
        self.current_token_index += quantity
        if (self.current_token_index <= len(self.tokens)-1):
            token = self.tokens[self.current_token_index]
            self.current_token_index -= quantity
            return token
        else:
            self.current_token_index -= quantity
            return Token(token='EMPTY', lexeme='', line=-99999)

    def read_token(self):
        self.current_token_index += 1
        if (self.current_token_index <= len(self.tokens)-1):
            return self.tokens[self.current_token_index]   
        else:
            self.current_token_index -= 1
            return Token(token='EMPTY', lexeme='', line=-99999)

    def is_identifier(self, token: Token):
        return token.token == 'IDENTIFIER'
    def is_boolean(self, token: Token):
        return (token.token == 'TRUE' or token.token == 'FALSE')
    def is_number(self, token: Token):
        return token.token == 'NUMERIC'
    def is_relation_op(self, token: Token):
        return (token.lexeme == '!=' or token.lexeme == '==' or token.lexeme == '<' or token.lexeme == '<=' or token.lexeme == '>' or token.lexeme == '>=')

    def semicolon(self): #ok
        token = self.read_token()
        if (not token.token == 'SEMICOLON'):
            raise ParserException(f"Faltou \";\" antes do {self.tokens[self.current_token_index].lexeme}", self.tokens[self.current_token_index].line)

    def identifier(self): # ok
        identifier = self.read_token() # read identifier
        if (not self.is_identifier(identifier)):
            raise ParserException(f"{identifier.lexeme} não é um nome de identificador válido", identifier.line)

    # --------START BODIES--------
    def program(self): # ok
        token = self.read_token() #read program

        if(not token.token =="HEADER_PROGRAM"): 
            raise ParserException(missing_token_exception_message("program"), token.line)

        self.identifier()
        self.set_symbol_type('PROGRAM_NAME')

        if (not self.read_token().token == "OPEN_BRACKET"): #read {
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.body()

        if (not self.read_token().token == "CLOSE_BRACKET"): #read }
            raise ParserException(missing_token_exception_message("}"), token.line)

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
        elif(self.is_identifier(token) and self.look_ahead().token == "OPEN_PARENTHESES"):
            self.current_token_index-=1
            self.function_call(True)
            function_call = True
        elif (not (self.is_identifier(token) or self.is_number(token) or self.is_boolean(token)) ):
            raise ParserException('Faltou fator', token.line)
        
        if (not function_call and self.is_identifier(token)): # a variable identifier was used
            self.set_symbol_type("VARIABLE_NAME")
        
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

        if (self.is_relation_op(self.look_ahead())):
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
    
    def var_declaration_block(self): # ok
        look_ahead = self.look_ahead()
        while (look_ahead.token == "INT_TYPE" or look_ahead.token == "BOOL_TYPE"):
            self.var_declaration()
            look_ahead = self.look_ahead()

    def var_declaration(self): # ok
        self.type()
        self.identifier()
        self.set_symbol_type("VARIABLE_NAME")

        while (self.look_ahead().lexeme==','):
            self.read_token() # read ,
            self.identifier()
            self.set_symbol_type("VARIABLE_NAME")

        self.semicolon()  

    def parameter(self): # ok
        self.type() 
        self.identifier()
        self.set_symbol_type("VARIABLE_NAME")

    def parameters_list(self): # ok
        look_ahead = self.look_ahead()
        if (look_ahead.token == "BOOL_TYPE" or look_ahead.token == "INT_TYPE"):
            self.parameter()  
            while (self.look_ahead().lexeme==','):
                self.read_token() # read ,
                self.parameter()
  
    def procedure_declaration(self): # ok 
        token = self.read_token() # read proc

        if (not token.token == "HEADER_PROC"):
            raise ParserException(f"Verificação com look ahead??? Era pra ler o proc", token.line)
        
        self.identifier()
        self.set_symbol_type("PROCEDURE_NAME")

        token = self.read_token() # read (
        if (not token.token == "OPEN_PARENTHESES"):
            raise ParserException(missing_token_exception_message("("), token.line)
        
        self.parameters_list()

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
        
    def function_declaration(self): # ok 
        token = self.read_token() # read func

        if (not token.token == "HEADER_FUNC"):
            raise ParserException(f"Verificação com look ahead??? Era pra ler o func", token.line)
        
        self.type()
        self.identifier()
        self.set_symbol_type("FUNCTION_NAME")

        token = self.read_token() # read (
        if (not token.token == "OPEN_PARENTHESES"):
            raise ParserException(missing_token_exception_message("("), token.line)
        
        self.parameters_list()

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

    # --------END DECLARATIONS--------

    # --------START COMMAND--------
    def commands(self): # ok
        self.command()
        while (self.look_ahead().token != "CLOSE_BRACKET"):
            
            self.command()

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
        self.identifier()
        self.set_symbol_type("VARIABLE_NAME")
        
        assign_op = self.read_token() # read =
        if (not (assign_op.token == 'ASSIGNMENT_OP')):
            raise ParserException(f"Atribuição inválida: {assign_op.lexeme}", assign_op.line)
        
        if(self.look_ahead().token == "INPUT_FUNC"):
            self.input_command()
        else:
            self.expression()
            self.semicolon()

    def print_command(self): # ok
        token = self.read_token() #read print

        if(not token.token =="PRINT_FUNC"): 
            raise ParserException(f"Verificação com look ahaed???", token.line)
        elif(not self.read_token().token == "OPEN_PARENTHESES"): #read (
            raise ParserException(missing_token_exception_message("("), token.line)

        self.expression()

        if (not self.read_token().token == "CLOSE_PARENTHESES"): #read )
            raise ParserException(missing_token_exception_message(")"), token.line)

        self.semicolon()

    def while_command(self): # ok
        token = self.read_token() #read while

        if(not token.token =="WHILE"): 
            raise ParserException(f"Verificação com look ahaed???", token.line)
        elif(not self.read_token().token == "OPEN_PARENTHESES"): #read (
            raise ParserException(missing_token_exception_message("("), token.line)

        self.expression()

        if (not self.read_token().token == "CLOSE_PARENTHESES"): #read )
            raise ParserException(missing_token_exception_message(")"), token.line)

        if (not self.read_token().token == "OPEN_BRACKET"): #read {
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.var_declaration_block()
        self.commands()

        if (not self.read_token().token == "CLOSE_BRACKET"): #read }
            raise ParserException(missing_token_exception_message("}"), token.line)
         
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
        if(not token.token == "RETURN"):
            raise ParserException(missing_token_exception_message("return"), token.line)
        self.expression()
        self.semicolon()            

    def sub_routine_call(self): # ok
        self.identifier()
        sub_routine_type = self.is_function_or_procedure(self.tokens[self.current_token_index].lexeme)
        self.set_symbol_type(sub_routine_type)

        token = self.read_token() # read (
        if (not token.token == 'OPEN_PARENTHESES'):
            raise ParserException(missing_token_exception_message("("), token.line)

        look_ahead = self.look_ahead() # check obrigatory ) or optionals expressions (separated by comma)
        while (not look_ahead.token == 'CLOSE_PARENTHESES'):
            self.expression()
            look_ahead = self.look_ahead() # check obrigatory ) or optional comma
            if (look_ahead.lexeme == ','):
                self.read_token() # read ,
        else:
            token = self.read_token() # read )
            if (not look_ahead.token == 'CLOSE_PARENTHESES'):
                raise ParserException(missing_token_exception_message(")"), token.line)

        self.semicolon()

    # only being called inside expression because outside an expression functions are called through sub_routine_call
    def function_call(self, in_expression = False): # ok 
        self.identifier()
        self.set_symbol_type("FUNCTION_NAME")

        token = self.read_token() # read (
        if (not token.token == 'OPEN_PARENTHESES'):
            raise ParserException(missing_token_exception_message("("), token.line)

        look_ahead = self.look_ahead() # check obrigatory ) or optionals expressions (separated by comma)
        while (not look_ahead.token == 'CLOSE_PARENTHESES'):
            self.expression()
            look_ahead = self.look_ahead() # check obrigatory ) or optional comma
            if (look_ahead.lexeme == ','):
                self.read_token() # read ,
        else:
            token = self.read_token() # read )
            if (not look_ahead.token == 'CLOSE_PARENTHESES'):
                raise ParserException(missing_token_exception_message(")"), token.line)

        if(not in_expression):
            self.semicolon()

    def conditional_command(self): # ok
        token = self.read_token() #read if

        if(not token.token == "IF"): 
            raise ParserException(f"Verificação com look ahaed???", token.line)
        elif(not self.read_token().token == "OPEN_PARENTHESES"): #read (
            raise ParserException(missing_token_exception_message("("), token.line)

        self.expression()

        if (not self.read_token().token == "CLOSE_PARENTHESES"): #read )
            raise ParserException(missing_token_exception_message(")"), token.line)

        if (not self.read_token().token == "OPEN_BRACKET"): #read {
            raise ParserException(missing_token_exception_message("{"), token.line)
        
        self.var_declaration_block()
        self.commands()

        if (not self.read_token().token == "CLOSE_BRACKET"): #read }
            raise ParserException(missing_token_exception_message("}"), token.line)

        if (self.look_ahead().token == "ELSE"):
            self.read_token() # read else
            if (not self.read_token().token == "OPEN_BRACKET"): #read {
                raise ParserException(missing_token_exception_message("{"), token.line)
            
            self.var_declaration_block()
            self.commands()

            if (not self.read_token().token == "CLOSE_BRACKET"): #read }
                raise ParserException(missing_token_exception_message("}"), token.line)

    
