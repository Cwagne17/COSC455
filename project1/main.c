#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

struct LEXEME {
    int ln_pos;
    int char_pos;
    char kind[10];
    char value[50];
}