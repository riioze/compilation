from typing import Optional, Tuple, List

from tokens import *
from node import *
from lexer import *
from parser import *
from optimizer import *
from code_gen import *

def main():
    code = ""

    files = [
        "std.c",
        "code.c"
    ]

    for file in files:
        with open(file,'r') as f:
            code+=f.read()+'\n'
    
    lexer = Lexer(code)
    lexer.next_token()
    parser = Parser(lexer)
    optimizer = Optimizer(parser)

    with open("msm/prg.asm",'w') as file:

        parser.begin()

        while(lexer.current_token.token_type != "tok_eof"):
            gencode(optimizer,file=file)

        parser.end()

        print(".start",file=file)
        print("prep main",file=file)
        print("call 0",file=file)
        print("halt",file=file)

        


if __name__ == "__main__":
    
    main()