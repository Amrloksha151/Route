from ply import lex # importing the lex lexer module

reserved = {
    # logical operators
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT",

    # control flow
    "BREAK": "BREAK",
    "ELIF": "ELIF",
    "ELSE": "ELSE",
    "FOR": "FOR",
    "IF": "IF",
    "IN": "IN",
    "WHILE": "WHILE",

    # functions / return
    "FUNC": "FUNCTION",
    "RETURN": "RETURN",

    # networking / protocols
    "ARP": "ARP",
    "HTTP": "HTTP",
    "ICMP": "ICMP",
    "SOCKET": "SOCKET",
    "TCP": "TCP",
    "UDP": "UDP",

    # commented / reserved for later
    # "CONTINUE": "CONTINUE",
    # "WS": "WS",
}

tokens = [
    # literals and identifiers
    "NUMBER",
    "TEXT",
    "BOOL",
    "IDENTIFIER",
    "NEWLINE",

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

    # grouping
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
] + list(reserved.values())