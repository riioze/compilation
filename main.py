from typing import Optional, Tuple, List

from tokens import *
from node import *
from lexer import *
from parser import *
from optimizer import *
from code_gen import *
from pathlib import Path
from sys import stdin,stdout


def load_code_from_file(in_file) -> str:


    code = ""

    files_paths = [
        Path("std.c")
    ]

    for file in files_paths:
        with open(file,'r') as f:
            code+=f.read()+'\n'
    
    code += in_file.read()

    return code

def compile_asm_in_file(in_code,out_file) -> None:

    lexer = Lexer(in_code)
    lexer.next_token()
    parser = Parser(lexer)
    optimizer = Optimizer(parser)

    parser.begin()

    while(lexer.current_token.token_type != "tok_eof"):
        gencode(optimizer,file=out_file)

    parser.end()

    print(".start",file=out_file)
    print("prep main",file=out_file)
    print("call 0",file=out_file)
    print("halt",file=out_file)

def main():

    in_code = load_code_from_file(stdin)
    compile_asm_in_file(in_code,stdout)


        


if __name__ == "__main__":
    
    main()
