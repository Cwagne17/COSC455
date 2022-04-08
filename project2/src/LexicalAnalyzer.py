from Lexeme import *
from symbol_table import *
    
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
