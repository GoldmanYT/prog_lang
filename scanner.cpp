#include <cstring>
#include <cstdio>
#include <vector>

using namespace std;

enum Code {
    lcProg,    // procedure15
    lcUsing,   // using15
    lcClass,   // class15
    lcStart,   // start15
    lcStop,    // stop15
    lcVar,     // var15
    lcWhile,   // while15
    lcTrue,    // true
    lcFalse,   // false
    lcSemi,    // ;
    lcColon,   // :
    lcDot,     // .
    lcOpPar,   // (
    lcClPar,   // )
    lcOpCurBr, // {
    lcClCurBr, // }
    lcAss,     // <-
    lcAdd,     // + | -
    lcMult,    // * | /
    lcNot,     // !
    lcAnd,     // &&
    lcOr,      // ||
    lcComp,    // < | > | <= | >= | = | /=
    lcId,      // identifier
    lcNum,     // number
    lcSp,      // space
    lcCom,     // commentary
    lcEof,     // end of file
    lcErr      // error
};

enum Attr {
    opAdd,  // +
    opSub,  // -
    opMult, // *
    opDiv,  // /
    opLt,   // <
    opGt,   // >
    opLe,   // <=
    opGe,   // >=
    opEq,   // =
    opNe    // /=
};

enum Category {
    catProgName,
    catTypeName,
    catVarName,
    catConst,
    catNoCat
};

enum TypeCode {
    typeVoid,
    typeInt,
    typeFloat,
    typeBoolean
};

struct Token {
    Code code;
    int attr;
    size_t start;
    size_t end;
};

struct TokenStack {
    size_t size = 0;
    Token tokens[1024];

    void push(Token token) {
        tokens[size++] = token;
    }

    void pop(Token token) {
        size--;
    }
};

int stateTable[][14] = {
//         [0]  [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9]  [10] [11] [12] [13]
/* tab */ { 10, -12, -28, -29, -16, -19, -20, -22, -30, -23,  10, -25,  12,  12},
/* lf  */ { 10, -12, -28, -29, -16, -19, -20, -22, -30, -23,  10, -25,  12,  12},
/* sp  */ { 10, -12, -28, -29, -16, -19, -20, -22, -30, -23,  10, -25,  12,  12},
/*  !  */ { -8, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  &  */ {  2, -12, -14, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  (  */ { -4, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  )  */ { -5, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  *  */ {-11, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  +  */ {-10, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  -  */ { 11, -12, -28, -29, -18, -19, -20, -22, -30, -23, -24,  12,  13, -26},
/*  .  */ { -3, -12, -28, -29, -16, -19, -20,   8, -30, -23, -24, -25,  12,  12},
/*  /  */ {  1, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  :  */ { -2, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  ;  */ { -1, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  <  */ {  4, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  =  */ { -9, -13, -28, -29, -17, -19, -21, -22, -30, -23, -24, -25,  12,  12},
/*  >  */ {  6, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  d  */ {  7, -12, -28, -29, -16,   5, -20,   7,   9,   9, -24, -25,  12,  12},
/*  l  */ {  5, -12, -28, -29, -16,   5, -20, -22, -30, -23, -24, -25,  12,  12},
/*  {  */ { -6, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  |  */ {  3, -12, -28, -15, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/*  }  */ { -7, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12},
/* oth */ {-27, -12, -28, -29, -16, -19, -20, -22, -30, -23, -24, -25,  12,  12}
};

char ErrMessages[][64] = {
    "Некорректный символ",
    "Ожидалось \"&\" после \"&\"",
    "Ожидалось \"|\" после \"|\"",
    "Ожидалась цифра после \".\"",
    "Ожидалось \"--\", встречен конец файла"
};

char keywords[][64] = {
    "procedure15",
    "using15",
    "class15",
    "start15",
    "stop15",
    "var15",
    "while15",
    "true", 
    "false"
};

Token stateToToken[] = {
/*   0 */ {Code(0), 0},
/*  -1 */ {lcSemi, 0},
/*  -2 */ {lcColon, 0},
/*  -3 */ {lcDot, 0},
/*  -4 */ {lcOpPar, 0},
/*  -5 */ {lcClPar, 0},
/*  -6 */ {lcOpCurBr, 0},
/*  -7 */ {lcClCurBr, 0},
/*  -8 */ {lcNot, 0},
/*  -9 */ {lcComp, opEq},
/* -10 */ {lcAdd, opAdd},
/* -11 */ {lcMult, opMult},
/* -12 */ {lcMult, opDiv},
/* -13 */ {lcComp, opNe},
/* -14 */ {lcAnd, 0},
/* -15 */ {lcOr, 0},
/* -16 */ {lcComp, opLt},
/* -17 */ {lcComp, opLe},
/* -18 */ {lcAss, 0},
/* -19 */ {lcId, 0},
/* -20 */ {lcComp, opGt},
/* -21 */ {lcComp, opGe},
/* -22 */ {lcNum, 0},
/* -23 */ {lcNum, 0},
/* -24 */ {lcSp, 0},
/* -25 */ {lcAdd, opSub},
/* -26 */ {lcCom, 0},
/* -27 */ {lcErr, 0},
/* -28 */ {lcErr, 1},
/* -29 */ {lcErr, 2},
/* -30 */ {lcErr, 3},
/* -31 */ {lcErr, 4}
};

int shiftBackTable[] = {
/*   0 */ 0,
/*  -1 */ 0,
/*  -2 */ 0,
/*  -3 */ 0,
/*  -4 */ 0,
/*  -5 */ 0,
/*  -6 */ 0,
/*  -7 */ 0,
/*  -8 */ 0,
/*  -9 */ 0,
/* -10 */ 0,
/* -11 */ 0,
/* -12 */ 1,
/* -13 */ 0,
/* -14 */ 0,
/* -15 */ 0,
/* -16 */ 1,
/* -17 */ 0,
/* -18 */ 0,
/* -19 */ 1,
/* -20 */ 1,
/* -21 */ 0,
/* -22 */ 1,
/* -23 */ 1,
/* -24 */ 1,
/* -25 */ 1,
/* -26 */ 0,
/* -27 */ 0,
/* -28 */ 0,
/* -29 */ 0,
/* -30 */ 0,
/* -31 */ 0
};

struct Symbol {
    char* lex;
    int cat;
    int type;
    int width;
};

vector<Symbol> symbolTable;

size_t charToTableIndex(char c) {
    if ('0' <= c && c <= '9') return 17;
    if ('A' <= c && c <= 'Z' ||
        'a' <= c && c <= 'z' ||
        c == -88 || c == -72 ||
        -64 <= c && c <= -1)
        return 18;
    switch (c) {
    case '\t': return 0;
    case '\n': return 1;
    case ' ': return 2;
    case '!': return 3;
    case '&': return 4;
    case '(': return 5;
    case ')': return 6;
    case '*': return 7;
    case '+': return 8;
    case '-': return 9;
    case '.': return 10;
    case '/': return 11;
    case ':': return 12;
    case ';': return 13;
    case '<': return 14;
    case '=': return 15;
    case '>': return 16;
    case '{': return 19;
    case '|': return 20;
    case '}': return 21;
    }
    return 22;
}

Token formToken(int state, Token& token, char* str) {
    Token result = token;

    result.code = stateToToken[-state].code;
    result.attr = stateToToken[-state].attr;

    if (result.code != lcId && result.code != lcNum) {
        return result;
    }

    bool isKeyword = false;
    for (int code = lcProg; code < sizeof(keywords) / sizeof(keywords[0]); code++) {
        if (strlen(keywords[code]) == result.end - result.start &&
                strncmp(keywords[code], str + result.start, strlen(keywords[code])) == 0) {
            result.code = Code(code);
            isKeyword = true;
            return result;
        }
    }
    bool isInSymbolTable = false;
    if (!isKeyword) {
        for (int i = 0; i < symbolTable.size(); i++) {
            if (strlen(symbolTable[i].lex) == result.end - result.start &&
                    strncmp(symbolTable[i].lex, str + result.start, strlen(symbolTable[i].lex)) == 0) {
                isInSymbolTable = true;
                result.attr = i;
                return result;
            }
        }
    }
    if (!isInSymbolTable) {
        char* lex = new char[result.end - result.start + 1] {};
        strncpy(lex, str + result.start, result.end - result.start);
        result.attr = symbolTable.size();
        symbolTable.push_back({ lex, 0, 0, 0 });
    }

    return result;
}

TokenStack* getTokens(char* code) {
    int state = 0;
    TokenStack* stack = new TokenStack;
    Token token {};

    for (size_t pos = 0; code[pos] != '\0'; pos++) {
        size_t row = charToTableIndex(code[pos]);
        state = stateTable[row][state];
        if (state < 0) {
            pos -= shiftBackTable[-state];
            token.end = pos + 1;
            token = formToken(state, token, code);
            state = 0;
            if (token.code != lcSp) {
                stack->push(token);
            }
            token.start = pos + 1;
        }
    }

    if (state == 12 || state == 13) {
        state = -31;
        token.end = strlen(code);
        token = formToken(state, token, code);
        stack->push(token);
    }

    return stack;
}

extern "C" {
    TokenStack* get_tokens(char* code) {
        return getTokens(code);
    }

    char* get_error_message(int i) {
        return ErrMessages[i];
    }

    size_t get_symbol_table_len() {
        return symbolTable.size();
    }

    Symbol get_symbol(int i) {
        return symbolTable[i];
    }
}
