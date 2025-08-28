from typing import Optional, Tuple




class Token :
    def __init__(self, token_type: str, token_pos: Tuple[int,int], token_value : Optional[int] = None, token_string : Optional[str] = None):
        self.token_type = token_type
        self.token_pos = token_pos
        self.token_value = token_value
        self.token_string = token_string
    
    def __str__(self):
        string = self.token_type + f" at ({self.token_pos})"

        if self.token_value:
            string += f" with value : {self.token_value}"
        if self.token_string:
            string += f" with string : {self.token_string}"
    
        return string





class Lexer:


    def __init__(self, text : str):
        self.pointer_pos = 0
        self.current_line = 0
        self.current_col = 0

        self.text = text

        self.current_token = Token("tok_start",(-1,-1))
        self.last_token = Token("tok_start",(-1,-1))

        self.spacing_chars = [
            ' ',
            '\n',
            '\t',
        ]

        self.keywords = [
            "int",
            "void",
            "return",
            "if",
            "else",
            "for",
            "do",
            "while",
            "break",
            "continue",
            "debug",
            "send",
            "rec"
        ]

    def test_eof(self):
        return self.pointer_pos == len(self.text)
            
    def eof_tok(self):
        return Token("tok_eof",(self.current_line,self.current_col))
    

    def is_number(self,character:str):
        return ord('0') <= ord(character) and ord(character) <= ord('9')
    
    def is_letter(self,character:str):
        return (ord('A') <= ord(character) and ord(character) <= ord('Z')) or (ord('a') <= ord(character) and ord(character) <= ord('z'))
    
    def is_alpha_num(self,character:str):
        return self.is_number(character) or self.is_letter(character)

    def next_token(self):
        
        self.last_token = self.current_token

        if self.test_eof():
            self.current_token = self.eof_tok()
            return

        while (self.text[self.pointer_pos] in self.spacing_chars): # skipping spaces
            self.pointer_pos += 1

            if self.test_eof():
                self.current_token = self.eof_tok()
                return

            self.current_col += 1
            if self.text[self.pointer_pos] == '\n':
                self.current_col = 0
                self.current_line+=1



        if self.is_number(self.text[self.pointer_pos]): # parse full number
            current_number = ''
            
            while not self.test_eof() and self.is_number(self.text[self.pointer_pos]):
                current_number += self.text[self.pointer_pos]
                self.pointer_pos+=1
                
            
            self.current_token = Token("tok_number",(self.current_line,self.current_col),token_value=int(current_number))
            return

        if self.is_letter(self.text[self.pointer_pos]):
            current_word = ''

            while not self.test_eof() and self.is_alpha_num(self.text[self.pointer_pos]):
                current_word += self.text[self.pointer_pos]
                self.pointer_pos+=1

            if current_word in self.keywords:
                self.current_token = Token("tok_"+current_word,(self.current_line,self.current_col),token_string=current_word)
            else:
                self.current_token = Token("tok_ident",(self.current_line,self.current_col),token_string=current_word)
            return
        
        match self.text[self.pointer_pos]:
            case '+':
                self.current_token = Token("tok_+",(self.current_line,self.current_col))

            case '-':
                self.current_token = Token("tok_-",(self.current_line,self.current_col))

            case '*':
                self.current_token = Token("tok_*",(self.current_line,self.current_col))

            case '/':
                self.current_token = Token("tok_/",(self.current_line,self.current_col))

            case '%':
                self.current_token = Token("tok_%",(self.current_line,self.current_col))
            
            case '&':
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '&':
                    self.current_token = Token("tok_&&",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_&",(self.current_line,self.current_col))
            
            case '|':
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '|':
                    self.current_token = Token("tok_||",(self.current_line,self.current_col))
                else:
                    throw_error(f"Token | unkown at pos (line = {self.current_line} col = {self.current_col}) did you mean \"||\" ?")
            
            case '!':
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_!=",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_!",(self.current_line,self.current_col))
            
            case '=':
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_==",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_=",(self.current_line,self.current_col))

            case '<':
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_<=",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_<",(self.current_line,self.current_col))

            case '>':
                if self.pointer_pos + 1 < len(self.text) and self.text[self.pointer_pos+1] == '=':
                    self.current_token = Token("tok_>=",(self.current_line,self.current_col))
                else:
                    self.current_token = Token("tok_<",(self.current_line,self.current_col))

            case '(':
                self.current_token = Token("tok_(",(self.current_line,self.current_col))

            case ')':
                self.current_token = Token("tok_)",(self.current_line,self.current_col))

            case '[':
                self.current_token = Token("tok_[",(self.current_line,self.current_col))

            case ']':
                self.current_token = Token("tok_]",(self.current_line,self.current_col))

            case '{':
                self.current_token = Token("tok_{",(self.current_line,self.current_col))

            case '}':
                self.current_token = Token("tok_}",(self.current_line,self.current_col))

            case ';':
                self.current_token = Token("tok_;",(self.current_line,self.current_col))

            case ',':
                self.current_token = Token("tok_,",(self.current_line,self.current_col))

            case other:
                throw_error(f"Token {other} unkown at pos (line = {self.current_line} col = {self.current_col})")
                

        
        

lexer = Lexer("^")

def throw_error(message:str):
    print(message)
    quit(1)

def accept(token_type:str):
    if not check(token_type):
        line, col = lexer.current_token.token_pos
        throw_error(f"wrong token at pos ({line = } {col = }) expected a token of type {token_type}")

def check(token_type:str):
    if lexer.current_token.token_type == token_type:
        lexer.next_token()
        return True
    return False

lexer.next_token()

print(lexer.current_token)
