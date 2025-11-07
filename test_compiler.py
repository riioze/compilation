from typing import TextIO
import subprocess
from pathlib import Path

test_codes = Path("tests")

def checking_function(in_code:TextIO,expected_text_out:bytes):

    p1 = subprocess.Popen(["python3", "main.py"],stdin=in_code,stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["./msm/msm"],stdin=p1.stdout,stdout=subprocess.PIPE)
    std_out,std_err = p2.communicate()
    assert std_out == expected_text_out

def test_base_loop():
    with open(test_codes/"test_base_loop.c" , 'r') as f:
        checking_function(f,b"0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n")

def test_nested_for_loop():
    with open(test_codes/"test_nested_for_loop.c" , 'r') as f:
        checking_function(f,b"0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n2\n3\n4\n5\n6\n7\n8\n9\n")

def test_fibo_rec():
    with open(test_codes/"test_fibo_rec.c" , 'r') as f:
        checking_function(f,b"144\n")

def test_nested_different_loops():
    with open(test_codes/"test_nested_different_loops.c", 'r') as f:
        checking_function(f,b"0\n1\n0\n2\n1\n0\n3\n2\n1\n0\n4\n3\n2\n1\n0\n")

def test_base_tabs():
    with open(test_codes/"test_base_tabs.c",'r') as f:
        checking_function(f,b"4\n3\n2\n1\n0\n")

def test_contexts():
    with open(test_codes/"test_contexts.c",'r') as f:
        checking_function(f,b"2\n1\n0\n")

def test_fibo_divide_conquer():
    with open(test_codes/"test_fibo_divide_conquer.c",'r') as f:
        checking_function(f,b"610\n")
