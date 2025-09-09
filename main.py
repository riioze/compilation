from typing import Optional, Tuple, List

from tokens import *
from node import *
from lexer import *
from parser import *
from optimizer import *
from code_gen import *

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

        print("halt",file=file)


if __name__ == "__main__":
    
    main()