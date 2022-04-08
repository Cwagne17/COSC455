from symbol_table import *

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
