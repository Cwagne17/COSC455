import os, logging

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ]
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
UNDERSCORE = "_"
SYNTAX_SPECIAL_CHARS = [":", ";", "(", ")", "<", ">", "=", "!", "/", "+", "-", "*"]

KEYWORDS = ["program", "end", "bool", "int", "if", "then", "else", "fi", "while", "do", "od", "print", "or", "and", "not", "false", "true"]
RELATIONAL_OPERATORS = [":=", "<", "=<", "=", "!=", ">=", ">"]
ARITHMETIC_OPERATORS = ["+", "-", "*", "/"]

COMMENT = "//"
NEWLINE = "\n"
WHITESPACE=" "

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

def recognizeID(ln, ln_num=0, char_pos=0):
    value=""
    kind="ID"
    position=char_pos
    
    while True:
        if not(ln[position]in LETTERS or ln[position] in UNDERSCORE or ln[position] in DIGITS): break
        value=value+ln[position]
        position+=1
        
    if value in KEYWORDS:
        kind=value
        
    return position+1, Lexeme(ln_num, char_pos, kind, value)

def recognizeNUM(ln, ln_num, char_pos):  
    value=""
    kind="NUM"
    position=char_pos
    
    while True:
        if ln[position] not in DIGITS: break
        value=value+ln[position]
        position+=1
        
    return position+1, Lexeme(ln_num, char_pos, kind, value)

def recognizeSPECIAL(ln, ln_num, char_pos):
    value=ln[char_pos]
    position=char_pos

    if position+1 < len(ln) and ln[position+1] not in [NEWLINE, WHITESPACE]:
        value = ln[char_pos: char_pos+2]
        
        if value == COMMENT: return len(ln), Lexeme(ln_num, char_pos, kind=COMMENT, value=COMMENT)
        
        elif value in RELATIONAL_OPERATORS: position+=2

    elif value != "/": position+=1
    
    else: print(f"\nln{ln_num}:{char_pos} Character is invalid, {value}"); exit()
    
    return position, Lexeme(ln_num, char_pos, kind=value, value=value)

def next(ln, ln_num=0, char_pos=0):
    # Skip whitespace
    while ln[char_pos] in [NEWLINE, WHITESPACE]: 
        if ln[char_pos] == NEWLINE: return char_pos+1, None
        char_pos+=1
    
    # Recognize next token
    char=ln[char_pos]
    if char in LETTERS: return recognizeID(ln, ln_num, char_pos)
    
    elif char in DIGITS: return recognizeNUM(ln, ln_num, char_pos)
    
    elif char in SYNTAX_SPECIAL_CHARS: return recognizeSPECIAL(ln, ln_num, char_pos)
    
    # Catch incorect character
    else: print(f"\nln{ln_num}:{char_pos} Character is invalid, {char}"); exit()
    

def main():
    with open("examples/if.txt") as fin:
        print("Position\tKind\t\tValue")
        for ln_num, ln in enumerate(fin.readlines()):
            char_pos=0
            while char_pos < len(ln):
                char_pos, token = next(ln, ln_num, char_pos)
                if token: print(f"{token.getPosition()}\t\t{token.kind}\t\t{token.value}")
        
main()    
        