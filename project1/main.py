import os, logging

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ]
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
UNDERSCORE = "_"

KEYWORDS = ["program", "end", 
            "bool", "int", 
            "if", "then", "else", "fi", 
            "while", "do", "od",
            "print", 
            "or", "and", "not", 
            "false", "true"]

SYNTAX_SPECIAL_CHARS = [":", ";", "(", ")", "<", ">", "=", "!", "/", "+", "-", "*"]

RELATIONAL_OPERATORS = [":=", "<", "=<", "=", "!=", ">=", ">"]
ARITHMETIC_OPERATORS = ["+", "-", "*", "/"]
COMMENT = "//"

NEWLINE = "\n"

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
    
    def getPosition(self):
        """Formats the position of the Lexeme

        Returns:
            str: formatted str
        """
        return f"ln{self.ln_num}:{self.char_pos}"

def recognizeID(ln, pos):
    i=pos
    token_val=""
    while True:
        if not(ln[i] in LETTERS or ln[i] in UNDERSCORE or ln[i] in DIGITS):
            break
        token_val=token_val+ln[i]
        i+=1
    kind="ID"
    if token_val in KEYWORDS:
        kind=token_val
    return i, kind, token_val

def recognizeNUM(ln, pos):  
    i=pos
    token_val=""
    while True:
        if ln[i] not in DIGITS:
            break
        token_val=token_val+ln[i]
        i+=1
    return i, "NUM", token_val

def recognizeSPECIAL(ln, pos):
    char=ln[pos]
    
    # Check for comment
    if char == "/" and len(ln)>pos+1:
        if ln[pos+1] == "/":
            return len(ln), "//", "//"
    
    # Check for arithmetic op
    if char in ARITHMETIC_OPERATORS:
        return pos+1, char, char
    
    # Check for Relop
    if len(ln)>pos+2:
        tmp=char+ln[pos+1]
        if tmp in RELATIONAL_OPERATORS:
            return pos+1, tmp, tmp
    elif char in RELATIONAL_OPERATORS:
        return pos+1, char, char
    
    return pos+1, char, char

def next(ln_num, ln):
    if ln is not None:
        i=0
        while i < len(ln)-1:
            char = ln[i]
            if char == NEWLINE or char == " ":
                i+=1
                continue
            elif char in LETTERS:
                end_pos, kind, value = recognizeID(ln, i)
                token = Lexeme(ln_num=ln_num, char_pos=i, kind=kind, value=value)
                i=end_pos
                print(token.getPosition(), token.kind, token.value)
            elif char in DIGITS:
                end_pos, kind, value = recognizeNUM(ln,i)
                token = Lexeme(ln_num=ln_num, char_pos=i, kind=kind, value=value)
                i=end_pos
                print(token.getPosition(), token.kind, token.value)
            elif char in SYNTAX_SPECIAL_CHARS: 
                end_pos, kind, value = recognizeSPECIAL(ln,i)
                token = Lexeme(ln_num=ln_num, char_pos=i, kind=kind, value=value)
                i=end_pos
                print(token.getPosition(), token.kind, token.value)
            else:
                i+=1
                logging.error(f"ln{ln_num}:{i} Character is invalid, {char}")
                exit()
            
            # print(i)
        # return Lexeme(ln_pos="", char_pos="", kind="", value="")

def main():
    with open("examples/ab3.txt") as fin:
        for ln_num, ln in enumerate(fin.readlines()):
            # print([char for char in ln])
            lex = next(ln_num, ln)
            # print(lex.getPosition(), lex.getKind(), lex.getValue())
        
main()    
        