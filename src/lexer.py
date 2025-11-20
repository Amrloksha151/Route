from ply import lex # importing the lex lexer module

tokens = (
    # literals and identifiers
    "NUMBER",
    "TEXT",
    "BOOL",
    "IDENTIFIER",

    # assignment and punctuation
    "ASSIGN",
    "COMMA",

    # arithmetic operators
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",

    # comparison operators
    "EQ",
    "NEQ",
    "LT",
    "GT",
    "LEQ",
    "GEQ",

    # logical operators
    "AND",
    "OR",
    "NOT",

    # grouping
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",

    # control flow keywords
    "IF",
    "ELIF",
    "ELSE",
    "WHILE",
    "FOR",
    "IN",
    "BREAK",
    # "CONTINUE",

    # functions and return
    "FUNCTION",
    "RETURN",

    # networking / protocols
    "SOCKET",
    "TCP",
    "UDP",
    "HTTP",
    "ARP",
    "ICMP",
    # "WS",
)