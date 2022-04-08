#! /usr/bin/env python3
"""Project 2: Syntax Analyzer

The syntax analyzer implements a top-down, predictive, recursive descent parser for it.
The parser should take an input file from the command line. Then it should return true if the input is correct syntactically according to “grammar.txt”.
As soon as a syntax error is encountered the parser should stop (terminate execution) and return the position of the error.

example command:
chmod +x src/project2.py; src/project2.py "examples/if.txt"
"""

import os, logging, sys
from symbol_table import *
from Lexeme import Lexeme
from LexicalAnalyzer import *

__author__ = "Christopher Wagner"
__credits__ = ["Christopher Wagner"]

__version__ = "1.0.0"
__maintainer__ = "Christopher Wagner"
__email__ = "cwagne17@students.towson.edu"
__status__ = "Development"

# --------------------------
# Project 2 Global Variables
# --------------------------

CHAR_POSITION=0
LINE_NUMBER=0
LINE=""
CURR_SYMBOL=None
   
# --------------------------
# Project 2 Section of code
# --------------------------


def match(symbol: str):
    if CURR_SYMBOL.kind != symbol:
        raise Exception(f"At position {getPosition(CURR_SYMBOL.ln_num, CURR_SYMBOL.char_pos)}, expected '{symbol}' but recieved {CURR_SYMBOL.kind}")
    next()
    
def expected(set_of_symbols: list[str]):
    if CURR_SYMBOL.kind not in set_of_symbols:
        raise Exception(f"At position {getPosition(CURR_SYMBOL.ln_num, CURR_SYMBOL.char_pos)}, expected '[{' | '.join(set_of_symbols)}]' but recieved {CURR_SYMBOL.kind}")

def program():
    match("program")
    match("ID")
    match(":")
    body()
    match("end")

def body():
    if CURR_SYMBOL.kind in ["bool", "int"]: declarations()
    statements()

def declarations():
    declaration()
    while CURR_SYMBOL.kind in ["bool", "int"]: declaration()

def declaration():
    expected(["bool", "int"])
    next()
    match("ID")
    match(";")

def statements():
    statement()
    while CURR_SYMBOL.kind == ";": statement()

def statement():
    if CURR_SYMBOL.kind == "ID": assignmentStatement()
    elif CURR_SYMBOL.kind == "if": conditionalStatement()
    elif CURR_SYMBOL.kind == "while": iterativeStatement()
    elif CURR_SYMBOL.kind == "print": printStatement()
    else: expected(["ID", "if", "while", "print"])

def assignmentStatement():
    expected(["ID"])
    next()
    match(":=")
    expression()

def expression():
    simpleExpression()
    if CURR_SYMBOL.kind in ["<", "=<", "=", "!=", ">=", ">"]:
        next()
        simpleExpression()

def simpleExpression():
    term()
    while CURR_SYMBOL.kind in ["+", "-", "or"]:
        next()
        term()

def term():
    factor()
    while CURR_SYMBOL.kind in ["*", "/", "and"]:
        next()
        factor()

def factor():
    if CURR_SYMBOL.kind in ["-", "not"]: next()
    if CURR_SYMBOL.kind in ["false", "true", "NUM"]: literal()
    elif CURR_SYMBOL.kind == "ID": next()
    elif CURR_SYMBOL.kind == "(":
        next()
        expression()
        match(")")
    else: expected(["-", "not", "false", "true", "NUM", "ID", "("])

def literal():
    expected(["true", "false", "NUM"])
    if CURR_SYMBOL.kind == "NUM": next()
    else: booleanLiteral()

def booleanLiteral():
    expected(["true", "false"])
    next()

def conditionalStatement():
    expected(["if"])
    next()
    expression()
    match("then")
    body()
    if CURR_SYMBOL.kind == "else":
        next()
        body()
    match("fi")

def iterativeStatement():
    expected(["while"])
    next()
    expression()
    match("do")
    body()
    match("od")

def printStatement():
    expected(["print"])
    next()
    expression()

"""
How to make an AST...

def term():
    tree:=factor()
    while curr_sym is multiplicative_operator:
        op:=curr_symbol
        next()
        tree2:=factor()
        tree:=node(op, tree, t2)
    return tree
"""

"""
Complete Error Parsing

1. extend functions to accept set of follow symbols for some non terminal symbol

def main():
    next()
    program(["end-of-text"])

def program(follow):
    match("program")
    match("ID")
    match(":")
    body(["end"])
    match("end")

def body(follow):
    if curr_sym is "bool" or "int":
        declarations(["ID", "if", "while", "print"])
    statements(follow)
    
def declarations(follow):
    declaration(follow U "bool" U "int")
    while curr_symbol is "bool" or "int":
        declaration(follow U "bool" U "int")
    expected(follow U "bool" or "int")
"""

# --------------------------
# Project 1 Next function
# --------------------------

def next():
    global CURR_SYMBOL, CHAR_POSITION, LINE_NUMBER, LINE
    
    # Skip whitespace
    while LINE[CHAR_POSITION] in [NEWLINE, WHITESPACE, TAB]: 
        if LINE[CHAR_POSITION] == NEWLINE: return len(LINE), None
        CHAR_POSITION+=1
    
    # Recognize next token
    char=LINE[CHAR_POSITION]
    if char in LETTERS: CHAR_POSITION, CURR_SYMBOL = recognizeID(LINE, LINE_NUMBER, CHAR_POSITION)
    
    elif char in DIGITS: CHAR_POSITION, CURR_SYMBOL = recognizeNUM(LINE, LINE_NUMBER, CHAR_POSITION)
    
    elif char in SYNTAX_SPECIAL_CHARS: CHAR_POSITION, CURR_SYMBOL = recognizeSPECIAL(LINE, LINE_NUMBER, CHAR_POSITION)
    
    # Catch incorect character
    else: invalidChar(LINE_NUMBER, CHAR_POSITION, char)
    
    if CURR_SYMBOL: print(f"{getPosition(CURR_SYMBOL.ln_num, CURR_SYMBOL.char_pos)}\t\t{CURR_SYMBOL.kind}\t\t{CURR_SYMBOL.value}")

# --------------------------
# Project 2 Runtime Section
# --------------------------

def main():
    global CHAR_POSITION, LINE_NUMBER, LINE, CURR_SYMBOL
    try:
        if len(sys.argv) != 2:
            print("File input not given.")
            exit()
        
        print("Position\tKind\t\tValue")
        
        with open(sys.argv[1]) as fin:
            for LINE_NUMBER, LINE in enumerate(fin.readlines()):
                CHAR_POSITION=0
                while CHAR_POSITION < len(LINE)-1:
                    next()
                    program()
            print(f"{getPosition(LINE_NUMBER, CHAR_POSITION)}\t\tend-of-text")
    except Exception as e:
        print(e)
if __name__ == "__main__":    
    main()
