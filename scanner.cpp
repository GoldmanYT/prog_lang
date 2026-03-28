#include <cstring>

enum Code {
    lcProg,    // procedure15
    lcUsing,   // using15
    lcClass,   // class15
    lcStart,   // start15
    lcStop,    // stop15
    lcVar,     // var15
    lcWhile,   // while15
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
    lcSp,      // space char
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

struct Token {
    Code code;
    void* attr;
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

Attr* attrs[10] = {
    new Attr(opAdd),  // +
    new Attr(opSub),  // -
    new Attr(opMult), // *
    new Attr(opDiv),  // /
    new Attr(opLt),   // <
    new Attr(opGt),   // >
    new Attr(opLe),   // <=
    new Attr(opGe),   // >=
    new Attr(opEq),   // =
    new Attr(opNe)    // /=
};

int stateTable[][14] = {
//         [0]  [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9]  [10] [11] [12] [13]
/* tab */ { 10, -12,  24,  23, -16, -19, -20, -22,  22, -23,  10, -25,  12,  12},
/* lf  */ { 10, -12,  24,  23, -16, -19, -20, -22,  22, -23,  10, -25,  12,  12},
/* sp  */ { 10, -12,  24,  23, -16, -19, -20, -22,  22, -23,  10, -25,  12,  12},
/*  !  */ { -8, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  &  */ {  2, -12, -14,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  (  */ { -4, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  )  */ { -5, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  *  */ {-11, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  +  */ {-10, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  -  */ { 11, -12,  24,  23, -18, -19, -20, -22,  22, -23, -24,  12,  13, -26},
/*  .  */ { -3, -12,  24,  23, -16, -19, -20,   8,  22, -23, -24, -25,  12,  12},
/*  /  */ {  1, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  :  */ { -2, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  ;  */ { -1, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  <  */ {  4, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  =  */ { -9, -13,  24,  23, -17, -19, -21, -22,  22, -23, -24, -25,  12,  12},
/*  >  */ {  6, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  d  */ {  7, -12,  24,  23, -16,   5, -20,   7,   9,   9, -24, -25,  12,  12},
/*  l  */ {  5, -12,  24,  23, -16,   5, -20, -22,  22, -23, -24, -25,  12,  12},
/*  {  */ { -6, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  |  */ {  3, -12,  24, -15, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/*  }  */ { -7, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12},
/* oth */ {-27, -12,  24,  23, -16, -19, -20, -22,  22, -23, -24, -25,  12,  12}
};

char ErrMessages[][64] = {
    "Invalid character",
    "Expected & after &",
    "Expected | after |",
    "Expected digit after .",
    "Commentary never closed",
};

char keywords[][64] = {
    "procedure15",
    "using15",
    "class15",
    "start15",
    "stop15",
    "var15",
    "while15"
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
/*  -9 */ {lcComp, attrs[opEq]},
/* -10 */ {lcAdd, attrs[opAdd]},
/* -11 */ {lcMult, attrs[opMult]},
/* -12 */ {lcMult, attrs[opDiv]},
/* -13 */ {lcComp, attrs[opNe]},
/* -14 */ {lcAnd, 0},
/* -15 */ {lcOr, 0},
/* -16 */ {lcComp, attrs[opLt]},
/* -17 */ {lcComp, attrs[opLe]},
/* -18 */ {lcAss, 0},
/* -19 */ {lcId, 0},
/* -20 */ {lcComp, attrs[opGt]},
/* -21 */ {lcComp, attrs[opGe]},
/* -22 */ {lcNum, 0},
/* -23 */ {lcNum, 0},
/* -24 */ {lcSp, 0},
/* -25 */ {lcAdd, attrs[opSub]},
/* -26 */ {lcCom, 0},
/* -27 */ {lcErr, ErrMessages[0]},
/* -28 */ {lcErr, ErrMessages[1]},
/* -29 */ {lcErr, ErrMessages[2]},
/* -30 */ {lcErr, ErrMessages[3]},
/* -31 */ {lcErr, ErrMessages[4]}
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
};


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

    for (int code = lcProg; code < 7; code++) {
        if (strlen(keywords[code]) == result.end - result.start &&
                strncmp(keywords[code], str + result.start, strlen(keywords[code])) == 0) {
            result.code = Code(code);
            break;
        }
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

    return stack;
}

extern "C" {
    TokenStack* get_tokens(char* code) {
        return getTokens(code);
    }
}
