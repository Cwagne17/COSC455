#! /usr/bin/env python3
"""Project 2: Syntax Analyzer

The syntax analyzer implements a top-down, predictive, recursive descent parser for it.
The parser should take an input file from the command line. Then it should return true if the input is correct syntactically according to “grammar.txt”.
As soon as a syntax error is encountered the parser should stop (terminate execution) and return the position of the error.

example command:
chmod +x src/project2.py; src/project2.py "examples/if.txt"
"""

import sys

__author__ = "Christopher Wagner"
__credits__ = ["Christopher Wagner"]

__version__ = "1.0.0"
__maintainer__ = "Christopher Wagner"
__email__ = "cwagne17@students.towson.edu"
__status__ = "Development"

# --------------------------
# Project 1 Global Variables
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
# Project 2 Global Variables
# --------------------------

CHAR_POSITION=0
LINE_NUMBER=0
CURR_SYMBOL=None
FILE_CONTENT=None

# --------------------------
# Project 1 Section of Code
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
    
    def __init__(self, ln_num: int, char_pos: int, kind: str, value):
        """constructor for Lexeme

        Args:
            ln_num (int): the line position of the token
            char_pos (int): the char position of the token on a given line
            kind (str): the kind, ID, NUM, or its value
            value (str | int): the characters that make up the token
        """
        self.ln_num = ln_num
        self.char_pos = char_pos
        self.kind = kind
        self.value = value
   
def getPosition(ln_num=0, char_pos=0):
    return f"{ln_num+1}:{char_pos+1}"

def invalidChar( ln_num=0, char_pos=0, char=""):
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
        
    return position, Lexeme(ln_num, char_pos, kind, int(value))

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
    while CURR_SYMBOL.kind == ";": 
        next()
        statement()

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

# --------------------------
# Project 1 Next function
# --------------------------

def next():
    global CURR_SYMBOL, CHAR_POSITION, LINE_NUMBER, FILE_CONTENT
    
    if CHAR_POSITION < len(FILE_CONTENT[LINE_NUMBER]):
        # Skip whitespace
        while FILE_CONTENT[LINE_NUMBER][CHAR_POSITION] in [NEWLINE, WHITESPACE, TAB]:
            if FILE_CONTENT[LINE_NUMBER][CHAR_POSITION] == NEWLINE:
                CHAR_POSITION = 0
                LINE_NUMBER += 1
                if LINE_NUMBER >= len(FILE_CONTENT): print('true'); exit()
            else: CHAR_POSITION+=1

        # Recognize next token
        line=FILE_CONTENT[LINE_NUMBER]
        char=line[CHAR_POSITION]
        
        if char in LETTERS: CHAR_POSITION, CURR_SYMBOL = recognizeID(line, LINE_NUMBER, CHAR_POSITION)
        
        elif char in DIGITS: CHAR_POSITION, CURR_SYMBOL = recognizeNUM(line, LINE_NUMBER, CHAR_POSITION)
        
        elif char in SYNTAX_SPECIAL_CHARS: CHAR_POSITION, CURR_SYMBOL = recognizeSPECIAL(line, LINE_NUMBER, CHAR_POSITION)
        
        # Catch incorect character
        else: invalidChar(LINE_NUMBER, CHAR_POSITION, char)
        
        if CURR_SYMBOL and CURR_SYMBOL.kind == COMMENT: CHAR_POSITION=0; LINE_NUMBER+=1; next()
        
        # if CURR_SYMBOL: print(f"{getPosition(CURR_SYMBOL.ln_num, CURR_SYMBOL.char_pos)}\t\t{CURR_SYMBOL.kind}\t\t{CURR_SYMBOL.value}")

# --------------------------
# Project 2 Runtime Section
# --------------------------

def main():
    global CHAR_POSITION, LINE_NUMBER, CURR_SYMBOL, FILE_CONTENT
    try:
        if len(sys.argv) != 2:
            print("File input not given.")
            exit()
        
        with open(sys.argv[1]) as fin:
            FILE_CONTENT = fin.readlines()
            if len(FILE_CONTENT) == 0:
                print("File is empty.") 
                exit()
        next()
        program()
    except Exception as e:
        print('false')
        print(e)

if __name__ == "__main__":    
    main()
