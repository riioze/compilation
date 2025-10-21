from typing import Optional, Tuple, List

from tokens import *
from node import *
from lexer import *
from parser import *
from optimizer import *
from code_gen import *
from pathlib import Path
from sys import stdin,stdout

def main():
    code = ""

    files_paths = [
        Path("std.c")
    ]

    for file in files_paths:
        with open(file,'r') as f:
            code+=f.read()+'\n'
    
    in_file = stdin
    code += in_file.read()

    lexer = Lexer(code)
    lexer.next_token()
    parser = Parser(lexer)
    optimizer = Optimizer(parser)

    out_file = stdout

    parser.begin()

    while(lexer.current_token.token_type != "tok_eof"):
        gencode(optimizer,file=out_file)

    parser.end()

    print(".start",file=out_file)
    print("prep main",file=out_file)
    print("call 0",file=out_file)
    print("halt",file=out_file)

        


if __name__ == "__main__":
    
    main()