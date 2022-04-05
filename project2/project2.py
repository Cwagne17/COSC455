#! /usr/bin/env python3
"""Project 2: Syntax Analyzer

The syntax analyzer implements a top-down, predictive, recursive descent parser for it.
The parser should take an input file from the command line. Then it should return true if the input is correct syntactically according to “grammar.txt”.
As soon as a syntax error is encountered the parser should stop (terminate execution) and return the position of the error.

example command:
chmod +x project2.py; ./project2.py "examples/if.txt"
"""

import os, logging, sys

__author__ = "Christopher Wagner"
__credits__ = ["Christopher Wagner"]

__version__ = "1.0.0"
__maintainer__ = "Christopher Wagner"
__email__ = "cwagne17@students.towson.edu"
__status__ = "Development"

# --------------------------
# Mock Symbol Table
# --------------------------

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ]
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
UNDERSCORE = "_"

SYNTAX_SPECIAL_CHARS = [":", ";", "(", ")", "<", ">", "=", "!", "/", "+", "-", "*"]
TWO_DIGIT_SPECIAL_CHARS = [":=", "=<", "!=", ">=", "//"]

KEYWORDS = ["program", "end", "bool", "int", "if", "then", "else", "fi", "while", "do", "od", "print", "or", "and", "not", "false", "true"]

COMMENT="//"
NEWLINE="\n"
WHITESPACE=" "
TAB="\t"

# --------------------------
# Project 1 Section of code
# --------------------------

class Lexeme:
    """Type for identifying tokens in mini-language's lexical analyzer

    Returns:
        obj: Type with position, kind, and value 
    """
    ln_num = 0
    char_pos = 0
    kind = ""
    value = ""
    
    def __init__(self, ln_num: int, char_pos: int, kind: str, value: str):
        """constructor for Lexeme

        Args:
            ln_num (int): the line position of the token
            char_pos (int): the char position of the token on a given line
            kind (str): the kind, ID, NUM, or its value
            value (str): the characters that make up the token
        """
        self.ln_num = ln_num
        self.char_pos = char_pos
        self.kind = kind
        self.value = value

def getPosition(ln_num=0, char_pos=0):
    return f"{ln_num+1}:{char_pos+1}:"

def invalidChar(ln_num=0, char_pos=0, char=""):
    print(f"{getPosition(ln_num, char_pos)} Character is invalid, {char}")
    exit()

def recognizeID(ln, ln_num=0, char_pos=0):
    value=""
    kind="ID"
    position=char_pos
    
    while position < len(ln):
        if not(ln[position]in LETTERS or ln[position] in UNDERSCORE or ln[position] in DIGITS): break
        value=value+ln[position]
        position+=1
    
    token = Lexeme(ln_num, char_pos, value, "") if value in KEYWORDS else Lexeme(ln_num, char_pos, kind, value)
        
    return position, token

def recognizeNUM(ln, ln_num, char_pos):  
    value=""
    kind="NUM"
    position=char_pos
    
    while position < len(ln):
        if ln[position] not in DIGITS: break
        value=value+ln[position]
        position+=1
        
    return position, Lexeme(ln_num, char_pos, kind, value)

def recognizeSPECIAL(ln, ln_num, char_pos):
    value=ln[char_pos]
    position=char_pos
    
    if position+1 < len(ln) and ln[position+1] not in [NEWLINE, WHITESPACE, TAB] and ln[position: position+2] in TWO_DIGIT_SPECIAL_CHARS:
        value = ln[char_pos: char_pos+2]
        
        if value == COMMENT: return len(ln), Lexeme(ln_num, char_pos, kind=COMMENT, value="")
        
        position+=2

    elif value not in ["!"]: position+=1
    
    else: invalidChar(ln_num, char_pos, value)
    
    return position, Lexeme(ln_num, char_pos, kind=value, value="")

def next(ln, ln_num=0, char_pos=0):
    # Skip whitespace
    while ln[char_pos] in [NEWLINE, WHITESPACE, TAB]: 
        if ln[char_pos] == NEWLINE: return len(ln), None
        char_pos+=1
    
    # Recognize next token
    char=ln[char_pos]
    if char in LETTERS: return recognizeID(ln, ln_num, char_pos)
    
    elif char in DIGITS: return recognizeNUM(ln, ln_num, char_pos)
    
    elif char in SYNTAX_SPECIAL_CHARS: return recognizeSPECIAL(ln, ln_num, char_pos)
    
    # Catch incorect character
    else: invalidChar(ln_num, char_pos, char)
    
    
# --------------------------
# Project 2 Section of code
# --------------------------

def statement():
    print('not yet implemented.')

def op():
    print('not yet implemented.')

def match():
    print('not yet implemented.')

# --------------------------
# Project 2 Runtime Section
# --------------------------

def main():
    FILE = sys.argv[1] if sys.argv[1] else "examples/if.txt"
    
    with open(FILE) as fin:
        print("Position\tKind\t\tValue")
        for ln_num, ln in enumerate(fin.readlines()):
            char_pos=0
            while char_pos < len(ln):
                char_pos, token = next(ln, ln_num, char_pos)
                if token: print(f"{getPosition(token.ln_num, token.char_pos)}\t\t{token.kind}\t\t{token.value}")
        print(f"{getPosition(ln_num, char_pos)}\t\tend-of-text")

if __name__ == "__main__":    
    main()
