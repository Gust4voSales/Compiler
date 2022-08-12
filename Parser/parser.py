from logging import raiseExceptions
from shutil import ExecError
from Token import Token
from Identifier import Identifier

class Parser:
    def __init__(self, tokens:list[Token], ids_table:list[Identifier]) -> None:
        self.tokens = tokens
        self.ids_table = ids_table
        self.current_token_index = -1
    
    def look_ahead(self):
        self.current_token_index += 1
        token = self.tokens[self.current_token_index]
        self.current_token_index -= 1
        return token

    def read_token(self):
        self.current_token_index += 1
        return self.tokens[self.current_token_index]   

    def expression (self):
        token = self.read_token()

    def variable(self, token):
        
        if (not token.token == 'IDENTIFIER'):
            return False 
        return True
    def number(self, token):
        return token.token == 'NUMERIC'


    def factor(self):
        token = self.read_token()  
        if  (self.variable(token)):
            return True
        if(self.number(token)):
            return True
        raise Exception('Faltou fator')
        
    def term(self): # ok 
        self.factor()
        #print(self.look_ahead())
        while (self.look_ahead().lexeme == '*' or self.look_ahead().lexeme == '/' or self.look_ahead().lexeme == '&&' ):
            self.terml()
            #print(self.tokens[self.current_token_index])
        else:
            print(f'Operador invalido {self.tokens[self.current_token_index]}')
        # if(not self.factor()):
        #     raise Exception('falor')

    def terml(self): # ok
        token = self.read_token()
        self.factor()
       
       
           
