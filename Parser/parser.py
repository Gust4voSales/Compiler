from Parser.ParserException import ParserException
from Token import Token
from Identifier import Identifier

class Parser:
    def __init__(self, tokens:list[Token], ids_table:list[Identifier]) -> None:
        self.tokens = tokens
        self.ids_table = ids_table
        self.current_token_index = -1
    
    def look_ahead(self):
        self.current_token_index += 1
        if (self.current_token_index <= len(self.tokens)-1):
            token = self.tokens[self.current_token_index]
            self.current_token_index -= 1
            return token
        else:
            self.current_token_index -= 1
            return Token(token='EMPTY', lexeme='', line=0)

    def read_token(self):
        self.current_token_index += 1
        if (self.current_token_index <= len(self.tokens)-1):
            print(self.tokens[self.current_token_index])    
            return self.tokens[self.current_token_index]   
        else:
            self.current_token_index -= 1
            return Token(token='EMPTY', lexeme='', line=0)

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
            raise ParserException(f"expressão inválida ao ler {self.tokens[self.current_token_index].lexeme}", self.tokens[self.current_token_index].line)

    def identifier(self):
        identifier = self.read_token() # read identifier
        if (not self.is_identifier(identifier)):
            raise ParserException(f"{identifier.lexeme} não é um nome de identificador válido", identifier.line)

    # --------START EXPRESSION--------
    def factor(self): 
        token = self.read_token()  

        # (<expression>) 
        if (token.lexeme=='('):
            self.expression()
            token = self.read_token()  
            if (not (token.lexeme==')')):
                raise ParserException("Faltou ')'", token.line)
        
        elif (not (self.is_identifier(token) or self.is_number(token) or self.is_boolean(token)) ):
            raise ParserException('Faltou fator', token.line)
        
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
    
    # --------START VARIABLES--------
    def type(self): # ok
        token = self.read_token()
        if (not (token.token == 'INT_TYPE' or token.token == 'BOOL_TYPE')):
            raise ParserException(f"Tipo {token.lexeme} inválido", token.line)

    def var_declaration(self): # ok
        self.type()
        self.identifier()

        while (self.look_ahead().lexeme==','):
            self.read_token() # read ,
            self.identifier()

        self.semicolon()

    def var_attribution(self):
        self.identifier()
        
        assign_op = self.read_token() # read =
        if (not (assign_op.token == 'ASSIGNMENT_OP')):
            raise ParserException(f"Atribuição inválida: {assign_op.lexeme}", assign_op.line)
        
        self.expression()

        self.semicolon()

    # --------END VARIABLES--------
