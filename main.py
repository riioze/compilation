from typing import Optional, Tuple, List




class Token :
    def __init__(self, token_type: str, token_pos : Tuple[int,int], token_value : Optional[int] = None, token_string : Optional[str] = None):
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


class Node:
     
    def __init__(self, node_type:str,node_pos: Tuple[int,int], node_value : Optional[int] = None, node_string: Optional[str] = None, children: List['Node'] = []):
        self.node_type = node_type
        self.node_pos = node_pos
        self.node_value = node_value
        self.node_string = node_string
        self.children = children


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
                
            
            self.current_token = Token("tok_const",(self.current_line,self.current_col),token_value=int(current_number))
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
                    raise ValueError(f"Token | unkown at pos (line = {self.current_line} col = {self.current_col}) did you mean \"||\" ?")
            
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
                raise ValueError(f"Token {other} unkown at pos (line = {self.current_line} col = {self.current_col})")

        self.pointer_pos += 1


    def accept(self,token_type:str):
        if not self.check(token_type):
            line, col = self.current_token.token_pos
            raise ValueError(f"wrong token at pos ({line = } {col = }) expected a token of type {token_type}")

    def check(self,token_type:str):
        if self.current_token.token_type == token_type:
            self.next_token()
            return True
        return False
                
class Parser:

    def __init__(self,lexer:Lexer):
        self.lexer = lexer
        
    
    def next_tree(self):
        return self.get_expression()
    
    def get_expression(self) -> Node:
        return self.get_prefix()

    def get_suffix(self) -> Node:
        return self.get_atom()

    def get_prefix(self) -> Node:
        if self.lexer.check("tok_!"):
            token_not = self.lexer.last_token
            intern_prefix = self.get_prefix()
            node_not = Node("nd_not",node_pos=token_not.token_pos,children=[intern_prefix])
            return node_not
        
        elif self.lexer.check("tok_-"):
            token_neg = self.lexer.last_token
            intern_prefix = self.get_prefix()
            node_neg = Node("nd_neg",node_pos=token_neg.token_pos,children=[intern_prefix])
            return node_neg
        
        elif self.lexer.check("tok_+"):
            return self.get_prefix()
        
        else:
            return self.get_suffix()

    def get_atom(self) -> Node:
        if self.lexer.check("tok_const"):
            token = self.lexer.last_token
            return Node("nd_const",node_pos=token.token_pos,node_value=token.token_value)

        elif self.lexer.check("tok_("):
            expression = self.get_expression()
            self.lexer.accept("tok_)")
            return expression
        
        else:
            raise ValueError(f"error at pos {self.lexer.current_token.token_pos}, expected const of expression")

    

class Optimizer:
    def __init__(self,parser:Parser):
        self.parser = parser
    
    def next_tree(self):
        return self.parser.next_tree()

def gencode(optimizer:Optimizer,file):
    tree = optimizer.next_tree()
    gennode(tree,file)

def gennode(node:Node,file):
    
    match node.node_type:
        case "nd_const":
            print(f"push {node.node_value}",file=file)

        case "nd_not":
            assert len(node.children) == 1, f"node nd_not at pos {node.node_pos} has not the required number of children (1)"
            gennode(node.children[0],file)
            print("not",file=file)
        
        case "nd_neg":
           assert len(node.children) == 1, f"node nd_not at pos {node.node_pos} has not the required number of children (1)"
           print("push 0",file=file)
           gennode(node.children[0],file)
           print("sub", file=file)
        
        case other:
            raise ValueError(f"node_type {other} at pos {node.node_pos} unknown")



        
def main():
    with open("code.c", 'r') as f:
        code = f.read()
    
    lexer = Lexer(code)
    lexer.next_token()
    parser = Parser(lexer)
    optimizer = Optimizer(parser)

    with open("msm/prg.asm",'w') as file:

        

        print(".start",file=file)

        while(lexer.current_token.token_type != "tok_eof"):
            gencode(optimizer,file=file)

        print("dbg",file=file)
        print("halt",file=file)





if __name__ == "__main__":
    main()